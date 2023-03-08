import numpy as np

from objects.Object import Object
from Ray import Ray, Ray_Collision
from vector_utils import normalized

class Polygon(Object):
	def __init__(self, vertices):
		super().__init__()

		assert len(vertices) >= 3, "Polygon must have at least 3 vertices"

		self.__vertices = vertices

		v1 = normalized(vertices[0] - vertices[1])
		v2 = normalized(vertices[2] - vertices[1])

		self.__normal = np.cross(v1, v2)

	def vertices(self):
		return self.__vertices

	def normal(self, point: np.ndarray) -> np.ndarray:
		return __normal

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		#NotImplemented # TODO
		return None
