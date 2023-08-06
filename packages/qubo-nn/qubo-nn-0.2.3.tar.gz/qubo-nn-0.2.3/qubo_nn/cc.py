import numpy as np


x = np.array([66, 92, 98, 17, 83, 57, 86, 97, 96, 47, 73, 32])
sol = [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1]

sols = [
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
]

for sol in sols:
    mask = x.copy()
    mask = np.zeros(x.shape, dtype='bool')
    mask[np.where(sol)] = True
    print(x[mask].sum())

    mask = np.ones(x.shape, dtype='bool')
    mask[np.where(sol)] = False
    print(x[mask].sum())
