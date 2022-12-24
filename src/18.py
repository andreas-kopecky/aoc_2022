import numpy as np
import pandas as pd

from scipy.ndimage import binary_fill_holes
from scipy.spatial.distance import pdist


def surface(coordinates: np.array) -> int:
    D = pdist(coordinates, metric="cityblock")
    D[D != 1] = 0
    return coordinates.shape[0] * 6 -  2 * D.sum()

def solve() -> tuple[int, int]:
    df = pd.read_csv("../data/18_input.txt", header=None)
    part_1 = surface(df.values)

    # Create empty space
    void = np.zeros(df.max().values + 1)
    # Put in all bocks at their coordinate positions and fill holes
    void[tuple(df.values.T)] = 1
    void_filled = binary_fill_holes(void)
    # Convert back to coordinate list that can be used for surface calculation like before
    filled_coordinates = np.vstack(np.where(void_filled == 1)).T
    part_2 = surface(filled_coordinates)
    return part_1, part_2


if __name__ == "__main__":
    print(solve())