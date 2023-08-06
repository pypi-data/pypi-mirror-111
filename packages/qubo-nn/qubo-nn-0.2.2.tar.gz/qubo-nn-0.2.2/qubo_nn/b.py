import random

import dimod.serialization.format
import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
from dwave_qbsolv import QBSolv
from networkx.generators.random_graphs import gnm_random_graph

from qubo_nn.problems import MaxCut
from qubo_nn.problems import MinimumVertexCover
from qubo_nn.problems import NumberPartitioning


SEED = 123


dimod.serialization.format.set_printoptions(depth=40)
np.set_printoptions(suppress=True)
np.random.seed(SEED)


def solve_qubo(qubo):
    qb = QBSolv()

    Q = {}
    # We can assume a quadratic matrix.
    for i in range(qubo.shape[0]):
        for j in range(qubo.shape[1]):
            if qubo[i][j] != 0:
                Q[(i, j)] = qubo[i][j]
    response = qb.sample_qubo(Q, num_repeats=1000, n_solutions=40, seed=SEED)
    print(response)

    for i in range(len(response.samples())):
        ret = [0] * len(response.samples()[0])
        for k, v in response.samples()[i].items():
            ret[k] = v
        print(ret)
    return ret


def modify_qubo1(qubo):
    for i in range(len(qubo)):
        for j in range(len(qubo)):
            if qubo[i][j] == 0:
                if random.random() > 0.9:
                    qubo[i][j] = 1.
    return qubo


G = gnm_random_graph(16, 20, seed=SEED)
# nx.draw(G)
# plt.show()

mc = MaxCut({}, G)
qubo = -mc.gen_qubo_matrix() + 0
print(qubo)
print(solve_qubo(qubo))
noise = np.random.random(size=qubo.shape) / 100.
np.fill_diagonal(noise, 0.)
qubo += noise
print(solve_qubo(qubo))

mc = MinimumVertexCover({}, G)
# qubo = mc.gen_qubo_matrix()
# print(qubo)
# print(solve_qubo(qubo))
# print(solve_qubo(qubo / 4))

# prob = np.random.randint(0, 100, (12,))
# print(prob.tolist())
# mc = NumberPartitioning({}, prob)
# qubo = mc.gen_qubo_matrix()
# print(qubo.min())
# qubo /= -qubo.min()
# # qubo /= 1000
# print(qubo.max())
# print(qubo)
# # print(solve_qubo(qubo * 1000))
# print(solve_qubo(qubo))
