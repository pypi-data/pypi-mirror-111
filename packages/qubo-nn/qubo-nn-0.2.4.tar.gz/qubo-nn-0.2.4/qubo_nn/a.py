import random

import networkx as nx
import matplotlib.pyplot as plt
from dwave_qbsolv import QBSolv
from networkx.generators.random_graphs import gnm_random_graph

from qubo_nn.problems.max_cut import MaxCut


def solve_qubo(qubo):
    qb = QBSolv()

    Q = {}
    # We can assume a quadratic matrix.
    for i in range(qubo.shape[0]):
        for j in range(qubo.shape[1]):
            if qubo[i][j] != 0:
                Q[(i, j)] = qubo[i][j]
    response = qb.sample_qubo(Q, num_repeats=1000)
    print(response)
    ret = [0] * len(response.samples()[0])
    for k, v in response.samples()[0].items():
        ret[k] = v
    return ret


def modify_qubo1(qubo):
    for i in range(len(qubo)):
        for j in range(len(qubo)):
            if qubo[i][j] == 0:
                if random.random() > 0.9:
                    qubo[i][j] = 1.
    return qubo


G = gnm_random_graph(16, 20, seed=123)
# nx.draw(G)
# plt.show()

mc = MaxCut({}, G)
qubo = -mc.gen_qubo_matrix() + 0
print(qubo)
qubo = modify_qubo1(qubo)
print(qubo)

solution = solve_qubo(qubo)
print(solution)
assert\
    solution == [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0] or\
    solution == [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1]
