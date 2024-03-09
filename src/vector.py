"Contains useful methods for manipulating numpy arrays as vectors."


import numpy as np
from numpy.typing import NDArray


def magnitude(vector: NDArray) -> float:
	"Returns the scalar length of the vector."

	assert vector.ndim == 1, f"A vector must be 1-dimensional, not {vector.ndim}-dimensional"
	return float(np.linalg.norm(vector))


	"Returns a new vector pointing in the same direction but with a length of 1 (or 0)."

def normalized(vector: NDArray) -> NDArray[np.float64]:
	mag = magnitude(vector)
	return vector / mag if mag != 0 else vector
