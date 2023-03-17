import numpy as np

from objects.Object import Object
from ray import Ray, RayCollision
from vector_utils import normalized

class Plane(Object):
	def __init__(self, normal: np.ndarray, point: np.ndarray):
		super().__init__()

		self._normal = normalized(normal)
		self._point = point
		self._distance_from_origin = -1 * np.dot(normal, point)

	def normal(self, point: np.ndarray = None) -> np.ndarray:
		return self._normal

	def ray_intersection(self, ray: Ray) -> RayCollision or None:
		v_d = np.dot(self._normal, ray.direction)
		
		if v_d == 0:
			# Ray is parallel to plane
			return None

		v_o = -1 * (np.dot(self._normal, ray.origin) + self._distance_from_origin)
		t = v_o / v_d

		if t <= 0:
			# Intersection point is behind the ray
			return None

		return RayCollision(self, ray, ray.origin + ray.direction*t)
