import numpy as np

from objects.Object import Object
from Ray import Ray, Ray_Collision
from vector_utils import normalized

class Plane(Object):
	def __init__(self, normal, point):
		super().__init__()

		self.__normal = normal
		self.__point = point
		self.__distance_from_origin = -1 * np.dot(normal, point)

	def normal(self, point: np.ndarray = None) -> np.ndarray:
		return self.__normal

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		v_d = np.dot(self.__normal, ray.direction)
		
		if v_d == 0:
			# Ray is parallel to plane
			return None

		v_o = -1 * (np.dot(self.__normal, ray.origin) + self.__distance_from_origin)
		t = v_o / v_d

		if t <= 0:
			# Intersection point is behind the ray
			return None

		return Ray_Collision(self, ray, ray.origin + ray.direction*t)
