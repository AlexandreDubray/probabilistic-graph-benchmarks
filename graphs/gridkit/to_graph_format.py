import re
import os

datasets = [
        'europe/Albania',
        'europe/Armenia',
        'europe/Austria',
        'europe/Belarus',
        'europe/Belgium',
        'europe/Bosnia and Herzegovina',
        'europe/Bulgaria',
        'europe/Croatia',
        'europe/Czech Republic',
        'europe/Denmark',
        'europe/Estonia',
        'europe/Finland',
        'europe/France',
        'europe/Georgia',
        'europe/Germany',
        'europe/Greece',
        'europe/Hungary',
        'europe/Iceland',
        'europe/Ireland',
        'europe/Italy',
        'europe/Latvia',
        'europe/Lithuania',
        'europe/Luxembourg',
        'europe/Montenegro',
        'europe/Netherlands',
        'europe/Norway',
        'europe/Poland',
        'europe/Portugal',
        'europe/Republic of Moldova',
        'europe/Romania',
        'europe/Russia',
        'europe/Serbia',
        'europe/Slovakia',
        'europe/Slovenia',
        'europe/Spain',
        'europe/Sweden',
        'europe/Switzerland',
        'europe/The former Yugoslav Republic of Macedonia',
        'europe/Turkey',
        'europe/Ukraine',
        'europe/United Kingdom',
        'north_america/Alabama',
        'north_america/Alaska',
        'north_america/Arizona',
        'north_america/Arkansas',
        'north_america/California',
        'north_america/Connecticut',
        'north_america/Delaware',
        'north_america/Florida',
        'north_america/Georgia',
        'north_america/Idaho',
        'north_america/Illinois',
        'north_america/Iowa',
        'north_america/Kansas',
        'north_america/Kentucky',
        'north_america/Louisiana',
        'north_america/Maine',
        'north_america/Maryland',
        'north_america/Massachusetts',
        'north_america/Michigan',
        'north_america/Minnesota',
        'north_america/Mississippi',
        'north_america/Missouri',
        'north_america/Montana',
        'north_america/Nebraska',
        'north_america/Nevada',
        'north_america/New Hampshire',
        'north_america/New Jersey',
        'north_america/New Mexico',
        'north_america/New York',
        'north_america/North Carolina',
        'north_america/North Dakota',
        'north_america/Ohio',
        'north_america/Oklahoma',
        'north_america/Oregon',
        'north_america/Pennsylvania',
        'north_america/Rhode Island',
        'north_america/South Carolina',
        'north_america/South Dakota',
        'north_america/Tennessee',
        'north_america/Texas',
        'north_america/Utah',
        'north_america/Vermont',
        'north_america/Virginia',
        'north_america/Washington',
        'north_america/West Virginia',
        'north_america/Wisconsin',
        'north_america/Wyoming',
]

_script_dir = os.path.dirname(os.path.realpath(__file__))

def parse_dataset(dataset):
    cur_id = 1
    node_map_id = {}
    with open(os.path.join(_script_dir, f'{dataset}/gridkit_{dataset.split("/")[1]}-highvoltage-vertices.csv')) as f:
        first = True
        for line in f:
            if first:
                first = False
                continue
            s = line.split(',')
            node_id = int(s[0])
            node_map_id[node_id] = cur_id
            cur_id += 1

    edges = []
    with open(os.path.join(_script_dir, f'{dataset}/gridkit_{dataset.split("/")[1]}-highvoltage-links.csv')) as f:
        first = True
        for line in f:
            if first:
                first = False
                continue
            s = line.split(',')
            edge_id = int(s[0])
            n1 = node_map_id[int(s[1])]
            n2 = node_map_id[int(s[2])]
            proba_up = 0.875
            edges.append((n1, n2, proba_up))
    return (cur_id - 1, edges)

def safe_str_bash(s):
    return re.sub('[\s $\#=!<>|;{}~&]', '_', s)

os.makedirs(os.path.join('graphs', 'europe'), exist_ok=True)
os.makedirs(os.path.join('graphs', 'north_america'), exist_ok=True)

for dataset in datasets:
    print(f'Processing {dataset}')
    s = dataset.split('/')
    continent = s[0]
    sub_region = safe_str_bash(s[1])
    dataset_input = f'{continent}/{sub_region}'
    (nb_nodes, edges) = parse_dataset(dataset_input)
    with open(os.path.join('graphs', continent, f'{sub_region}.graph'), 'w') as f:
        f.write(f'undirected {nb_nodes} {len(edges)}\n')
        f.write('\n'.join([f'{n1} {n2} {p}' for (n1, n2, p) in edges]))
