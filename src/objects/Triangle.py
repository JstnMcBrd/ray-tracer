import numpy as np

from objects.Plane import Plane
from objects.Polygon import Polygon
from Ray import Ray, Ray_Collision
from vector_utils import magnitude, normalized


def triangle_area(v1: np.ndarray, v2: np.ndarray, v3: np.ndarray):
	return abs((v1[0] * (v2[1] - v3[1]) + v2[0] * (v3[1] - v1[1]) + v3[0] * (v1[1] - v2[1])) / 2.0)


class Triangle(Polygon):
	def __init__(self, vertices: list):
		super().__init__(vertices)

		assert len(vertices) == 3, "Triangle must have 3 vertices"

		self._flattened_area = triangle_area(self._flattened_vertices[0], self._flattened_vertices[1], self._flattened_vertices[2])

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		# See if ray intersects with plane
		plane_collision = self._plane.ray_intersection(ray)
		if plane_collision is None:
			return None
		intersection = plane_collision.position

		# All vertices are pre-flattened in Polygon.__init__()
		flattened_intersection = np.delete(intersection, self._plane_dominant_coord)

		# Calculate areas
		area_1 = triangle_area(self._flattened_vertices[0], self._flattened_vertices[1], flattened_intersection)
		area_2 = triangle_area(self._flattened_vertices[0], self._flattened_vertices[2], flattened_intersection)
		area_3 = triangle_area(self._flattened_vertices[1], self._flattened_vertices[2], flattened_intersection)

		# If point is inside triangle, then the area of all sub-triangles will add up to the total area
		if abs(area_1 + area_2 + area_3 - self._flattened_area) > 0.01:
			return None

		return Ray_Collision(self, ray, intersection)
