"""
Contains useful methods for manipulating numpy arrays as vectors.
"""


import numpy as np


def magnitude(vector: np.ndarray) -> float:
	""" Returns the scalar length of the vector. """

	return np.sqrt(np.dot(vector, vector))


def normalized(vector: np.ndarray) -> np.ndarray:
	""" Returns a new vector pointing in the same direction but with a length of 1 (or 0). """

	mag = magnitude(vector)
	return vector / mag if mag != 0 else vector
