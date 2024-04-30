import os

def graph_from_file(filename):
    with open(filename) as f:
        n_nodes = None
        n_edges = None
        edges = []
        for line in f:
            s = line.strip().split(' ')
            if n_nodes is None:
                n_nodes = int(s[1])
                n_edges = int(s[2])
                continue
            edges.append((int(s[0]), int(s[1]), float(s[2])))
        return {
                'n_nodes': n_nodes,
                'n_edges': n_edges,
                'edges': edges
                }

def sch(graph, outdir, queries):
    distributions = []
    clauses = []
    n_probabilistic_var = graph['n_edges']*2
    for edge_id, (n1, n2, p) in enumerate(graph['edges']):
        distributions.append(f'c p distribution {p} {1 - p}')
        edge_var = edge_id*2 + 1
        clauses.append(f'-{n1 + n_probabilistic_var} -{edge_var} {n2 + n_probabilistic_var} 0')
        clauses.append(f'-{n2 + n_probabilistic_var} -{edge_var} {n1 + n_probabilistic_var} 0')

    for (s, t) in queries:
        with open(os.path.join(outdir, f'{s}_{t}.cnf'), 'w') as f:
            f.write(f'p cnf {len(distributions)*2 + graph["n_nodes"]} {len(clauses) + 2}\n')
            f.write('\n'.join(distributions) + '\n')
            f.write('\n'.join(clauses) + '\n')
            f.write(f'{s + n_probabilistic_var} 0\n-{t + n_probabilistic_var} 0')


def pwmc(graph, outdir, queries):
    clauses = []
    weights = []
    projected_set = ' '.join([str(x + 1) for x in range(graph['n_edges'])])
    number_edge = graph['n_edges']
    for edge_id, (n1, n2, p) in enumerate(graph['edges']):
        clauses.append(f'-{n1 + number_edge} -{edge_id + 1} {n2 + number_edge} 0')
        clauses.append(f'-{n2 + number_edge} -{edge_id + 1} {n1 + number_edge} 0')
        weights.append(f'c p weight {edge_id + 1} {p} 0')
        weights.append(f'c p weight -{edge_id + 1} {1 - p} 0')

    for (s, t) in queries:
        with open(os.path.join(outdir, f'{s}_{t}.cnf'), 'w') as f:
            f.write(f'p cnf {graph["n_nodes"] + graph["n_edges"]} {len(clauses) + 2}\n')
            f.write(projected_set + '\n')
            f.write('\n'.join(weights) + '\n')
            f.write('\n'.join(clauses) + '\n')
            f.write(f'{s + number_edge} 0\n-{t + number_edge} 0')
