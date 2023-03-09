import numpy as np

# In this project, vectors are represented with 1x3 numpy arrays

def magnitude(vector: np.ndarray) -> float:
	return np.sqrt(np.dot(vector, vector))


def normalized(vector: np.ndarray) -> np.ndarray:
	mag = magnitude(vector)
	return vector / mag if mag != 0 else vector
