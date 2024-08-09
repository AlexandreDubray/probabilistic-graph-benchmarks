import os
import sys
import subprocess

def get_or_put(map, key, value):
    try:
        return map[key]
    except KeyError:
        map[key] = value
        return value

if __name__ == '__main__':

    if len(sys.argv) != 5 or '--help' in sys.argv or '-h' in sys.argv:
        print("This script can be used to compute the connectivity of two nodes in a probabilistic gaph.")
        print("Given such a graph, a source and target node, it computes, using a projected weighted model counter, the probability that they are disconnected")
        print()
        print("Usage: python pwmc.py [--help] <model.graph> <source> <target> <PWMC command>")
        print('\tmodel.graph: The input graph')
        print('\tsource: The source node')
        print('\ttarget: The target node')
        print('PWMC command: the command for the model counter. Use {} as a placeholder for the input file')
        sys.exit(1)

    model = sys.argv[1]

    map_node = {}
    variable_id = 1

    model = open(sys.argv[1]).read().split()
    if model[0] != 'DIRECTED' and model[0] != 'UNDIRECTED':
        print('Wrong format for the model, should start by either DIRECTED or UNDIRECCTED')
        sys.exit(1)

    clauses = []
    weights = []

    directed = model[0] == 'DIRECTED'
    number_edges = int((len(model) - 1) / 3)
    edge_index = 1
    i = 1
    while i < len(model):
        source = get_or_put(map_node, model[i], len(map_node) + number_edges + 1)
        target = get_or_put(map_node, model[i+1], len(map_node) + number_edges + 1)
        proba = float(model[i+2])
        clauses.append(f'-{source} -{edge_index} {target} 0')
        if not directed:
            clauses.append(f'-{target} -{edge_index} {source} 0')

        weights.append(f'c p weight {edge_index} {proba} 0')
        weights.append(f'c p weight -{edge_index} {1.0 - proba} 0')
        i += 3

    clauses.append(f'{map_node[sys.argv[2]]} 0')
    clauses.append(f'-{map_node[sys.argv[3]]} 0')

    with open('input.cnf', 'w') as f:
        f.write(f'p cnf {len(map_node) + number_edges} {len(clauses)}\n')
        f.write(f'c p ind {" ".join([str(x) for x in range(1, number_edges + 1)])} 0\n')
        f.write('\n'.join(weights) + '\n')
        f.write('\n'.join(clauses))

    subprocess.run(sys.argv[4].format('input.cnf').split())
    os.remove('input.cnf')
