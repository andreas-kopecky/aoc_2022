import numpy as np

from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import csgraph_masked_from_dense

np.set_printoptions(linewidth=200, threshold=5000, edgeitems=20)

moves = {
    ( 0, -1): [(-1, -1), ( 0, -1), ( 1, -1)],
    ( 0,  1): [( 1,  1), ( 0,  1), ( 1,  1)],
    (-1,  0): [(-1, -1), (-1,  0), (-1,  1)],
    ( 1,  0): []
}

def solve() -> tuple[int, int]:
    with open("../data/23_example.txt", "r") as fh:
        elves = fh.read()

    l = elves.index("\n")
    data = np.fromstring(elves, dtype=np.uint8).reshape(-1, l + 1)[:, :-1]
    data[data != ord("#")] = 0
    data[data == ord("#")] = 1

    coordinates = np.vstack(np.where(data == 1)).T
    D = pdist(coordinates, metric="chebyshev")
    G = csgraph_masked_from_dense(squareform(D == 1))
    print(G)
    print(np.sum(G, axis=1))
    print(np.any(G, axis=1))
    return 1, 1


if __name__ == "__main__":
    print(solve())
