"""
Classes to define the properties and behaviors of rays.
"""


import numpy as np

from vector import magnitude


class RayCollision:
	""" Contains information about the collision of a ray with an object. """

	def __init__(self, obj, ray, position: np.ndarray):
		self.obj = obj
		self.ray = ray
		self.position = position

		self.distance = magnitude(self.position - ray.origin)


class Ray:
	""" Represents a semi-infinite line. """

	def __init__(self, origin: np.ndarray, direction: np.ndarray):
		self.origin = origin
		self.direction = direction
