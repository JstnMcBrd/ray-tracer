import numpy as np

from objects.Object import Object
from objects.Plane import Plane
from Ray import Ray, Ray_Collision
from vector_utils import magnitude, normalized

class Circle(Object):
	def __init__(self, center: np.ndarray, radius: float, normal: np.ndarray):
		super().__init__()

		self.center = center
		self.radius = radius
		self.__normal = normalized(normal)

		self.__plane = Plane(self.__normal, center)

	def normal(self, point: np.ndarray = None) -> np.ndarray:
		return self.__normal

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		# See if ray intersects with plane
		plane_collision = self.__plane.ray_intersection(ray)
		if plane_collision is None:
			return None

		# Check if intersection is within circle radius
		intersection = plane_collision.position
		distance = magnitude(intersection - self.center)

		if distance > self.radius:
			return None

		return Ray_Collision(self, ray, intersection)
