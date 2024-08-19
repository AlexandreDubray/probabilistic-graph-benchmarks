import sys
import os
import random

random.seed(697458)

script_dir = os.path.dirname(os.path.realpath(__file__))
graph_dir = os.path.join(script_dir, 'graphs', 'gridkit', 'graphs')
europe_dir = os.path.join(graph_dir, 'europe')
usa_dir = os.path.join(graph_dir, 'north_america')
outdir = os.path.join(script_dir, 'bench-input')
os.makedirs(outdir, exist_ok=True)

def _get_queries(filename):
    with open(filename) as f:
        content = f.read().split()
        nodes = set()
        idx = 1
        while idx < len(content):
            nodes.add(content[idx])
            nodes.add(content[idx + 1])
            idx += 3
        nodes = list(nodes)
        queries = []

        random.shuffle(nodes)
        for i in range(min(5, int(len(nodes) / 2))):
            queries.append(f'{nodes[2*i]} {nodes[2*i+1]}')
        return queries

def make_opti_bench():
    instances = [os.path.join(europe_dir, f) for f in os.listdir(europe_dir) if os.path.isfile(os.path.join(europe_dir, f))] + [os.path.join(usa_dir, f) for f in os.listdir(usa_dir) if os.path.isfile(os.path.join(usa_dir, f))]
    with open(os.path.join(outdir, 'opti-benchs.csv'), 'w') as f:
        f.write('model,query')
        for model in instances:
            print(f'Processing {model}')
            f.write('\n')
            queries = _get_queries(model)
            f.write('\n'.join([f'{model},{query}' for query in queries]))

def make_learn_bench():
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python make_schlandals_benchmarks.py [opti|learn]")
        sys.exit(1)
    if sys.argv[1] == 'opti':
        make_opti_bench()
    elif sys.argv[1] == 'learn':
        make_learn_bench()
    else:
        print("Usage: python make_schlandals_benchmarks.py [opti|learn]")
        sys.exit(1)
