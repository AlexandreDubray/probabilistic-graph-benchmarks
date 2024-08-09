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
        print("Given such a graph, a source and target node, it computes, using problog, the probability that they are disconnected")
        print()
        print("Usage: python pl.py [--help] <model.graph> <source> <target> <problog command>")
        print('\tmodel.graph: The input graph')
        print('\tsource: The source node')
        print('\ttarget: The target node')
        print('\tproblog command: the command for problog. Use {} as a placeholder for the input file')
        sys.exit(1)

    model = sys.argv[1]

    map_node = {}
    variable_id = 1

    model = open(sys.argv[1]).read().split()
    if model[0] != 'DIRECTED' and model[0] != 'UNDIRECTED':
        print('Wrong format for the model, should start by either DIRECTED or UNDIRECCTED')
        sys.exit(1)

    edges = []

    directed = model[0] == 'DIRECTED'
    i = 1
    while i < len(model):
        source = get_or_put(map_node, model[i], len(map_node) + 1)
        target = get_or_put(map_node, model[i+1], len(map_node) + 1)
        proba = float(model[i+2])
        edges.append(f'{proba}::edge({source},{target}).')
        i += 3

    with open('input.pl', 'w') as f:
        f.write('\n'.join(edges) + '\n')
        f.write('path(X, Y) :- edge(X, Y).\n')
        f.write('path(X, Y) :- edge(X, Z), path(Z, Y).\n')
        if directed:
            f.write('edge(X, Y) :- edge(Y, X).\n')
        f.write(f'query(path({map_node[sys.argv[2]]},{map_node[sys.argv[3]]})).')

    subprocess.run(sys.argv[4].format('input.pl').split())
    os.remove('input.pl')
