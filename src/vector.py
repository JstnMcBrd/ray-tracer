"""Contains useful methods for manipulating numpy arrays as vectors."""


import numpy as np
from numpy.typing import NDArray


def magnitude(vector: NDArray) -> float:
	"""Return the scalar length of the vector."""
	if vector.ndim != 1:
		raise ValueError(f"A vector must be 1-dimensional, not {vector.ndim}-dimensional")
	return float(np.linalg.norm(vector))


def normalized(vector: NDArray) -> NDArray[np.float64]:
	"""Return a new vector with the same direction but with a length of 1 or 0."""
	mag = magnitude(vector)
	return vector / mag if mag != 0 else vector
