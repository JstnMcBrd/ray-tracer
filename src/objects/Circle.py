import numpy as np

from objects.Object import Object
from objects.Plane import Plane
from ray import Ray, RayCollision
from vector_utils import magnitude, normalized

class Circle(Object):
	def __init__(self, center: np.ndarray, radius: float, normal: np.ndarray):
		super().__init__()

		self.center = center
		self.radius = radius
		
		normal = normalized(normal)
		self._plane = Plane(normal, center)

	def normal(self, point: np.ndarray = None) -> np.ndarray:
		return self._plane.normal(point)

	def ray_intersection(self, ray: Ray) -> RayCollision or None:
		# See if ray intersects with plane
		plane_collision = self.__plane.ray_intersection(ray)
		if plane_collision is None:
			return None

		# Check if intersection is within circle radius
		intersection = plane_collision.position
		distance = magnitude(intersection - self.center)

		if distance > self.radius:
			return None

		return RayCollision(self, ray, intersection)
