"Classes to define the properties and behaviors of rays."


import numpy as np
from numpy.typing import NDArray
from vector import magnitude


class Ray:
	"Represents a semi-infinite line."

	origin: NDArray[np.float64]
	direction: NDArray[np.float64]

	def __init__(self, origin: NDArray[np.float64], direction: NDArray[np.float64],
		self.origin = origin
		self.direction = direction


class RayCollision:
	"Contains information about the collision of a ray with an object."

	# obj: Object # would cause a circular import
	ray: Ray
	position: NDArray[np.float64]
	distance: float

	def __init__(self, obj, ray: Ray, position: NDArray[np.float64]) -> None:  # noqa: ANN001
		self.obj = obj
		self.ray = ray
		self.position = position

		self.distance = magnitude(self.position - ray.origin)
