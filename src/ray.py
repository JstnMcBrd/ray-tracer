"""
Classes to define the properties and behaviors of rays.
"""


import numpy as np

from scene import Scene
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

	def cast(self, scene: Scene) -> RayCollision|None:
		""" Projects the ray into the scene and returns the closest object collision. """

		closest_collision: RayCollision = None

		# Find the closest object that intersects with the ray
		for obj in scene.objects:
			collision = obj.ray_intersection(self)
			if collision is not None:
				if closest_collision is None or collision.distance < closest_collision.distance:
					closest_collision = collision

		return closest_collision
