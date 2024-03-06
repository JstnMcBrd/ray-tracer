"Classes to define the properties and behaviors of rays."


import numpy as np

from vector import magnitude


class Ray:
	"Represents a semi-infinite line."

	origin: np.ndarray
	direction: np.ndarray

	def __init__(self, origin: np.ndarray, direction: np.ndarray):
		self.origin = origin
		self.direction = direction


class RayCollision:
	"Contains information about the collision of a ray with an object."

	# obj: Object # would cause a circular import
	ray: Ray
	position: np.ndarray
	distance: float

	def __init__(self, obj, ray: Ray, position: np.ndarray):
		self.obj = obj
		self.ray = ray
		self.position = position

		self.distance = magnitude(self.position - ray.origin)
