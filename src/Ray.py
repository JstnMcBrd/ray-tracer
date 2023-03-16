import numpy as np

from scene import Scene
from vector_utils import magnitude

class Ray_Collision:
	def __init__(self, obj, ray, position: np.ndarray):
		self.obj = obj
		self.ray = ray
		self.position = position
		
		self.distance = magnitude(self.position - ray.origin)


class Ray:
	def __init__(self, origin: np.ndarray, direction: np.ndarray):
		self.origin = origin
		self.direction = direction

	def cast(self, scene: Scene) -> Ray_Collision or None:
		closest_collision: Ray_Collision = None

		# Find the closest object that intersects with the ray
		for obj in scene.objects:
			collision = obj.ray_intersection(self)
			if collision is not None:
				if closest_collision is None or collision.distance < closest_collision.distance:
					closest_collision = collision
		
		return closest_collision
