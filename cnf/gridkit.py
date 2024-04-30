import random
random.seed(996534781)

import os
from graph_to_cnf import *

script_dir = os.path.dirname(os.path.realpath(__file__))
graphs_dir = os.path.join(script_dir, '..', 'graphs', 'gridkit', 'graphs')
pwmc_dir = os.path.join(script_dir, 'pwmc')
sch_dir = os.path.join(script_dir, 'sch')
os.makedirs(pwmc_dir, exist_ok=True)
os.makedirs(sch_dir, exist_ok=True)

for continent in ['europe', 'north_america']:
    os.makedirs(os.path.join(pwmc_dir, continent), exist_ok=True)
    os.makedirs(os.path.join(sch_dir, continent), exist_ok=True)
    for state in os.listdir(os.path.join(graphs_dir, continent)):
        state_name = state.split('.')[0]
        print(f'Handling {continent}/{state_name}')
        os.makedirs(os.path.join(pwmc_dir, continent, state_name), exist_ok=True)
        os.makedirs(os.path.join(sch_dir, continent, state_name), exist_ok=True)
        filename = os.path.join(graphs_dir, continent, state)
        graph = graph_from_file(filename)
        nodes = [i+1 for i in range(graph['n_nodes'])]
        random.shuffle(nodes)
        queries = []
        for i in range(min(5, int(len(nodes) / 2))):
            s = nodes[2*i]
            t = nodes[2*i + 1]
            queries.append((s,t))

        sch(graph, os.path.join(sch_dir, continent, state_name), queries)
        pwmc(graph, os.path.join(pwmc_dir, continent, state_name), queries)
