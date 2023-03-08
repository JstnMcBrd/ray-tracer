import numpy as np

from objects.Object import Object
from objects.Plane import Plane
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

		self.__plane = Plane(self.__normal, vertices[0])

		# Project all the vertices onto a 2D plane (for future intersection calculations)
		self.__plane_dominant_coord = np.where(np.abs(self.__normal) == np.max(np.abs(self.__normal)))[0][0]
		self.__flattened_vertices = [np.append(np.delete(v, self.__plane_dominant_coord), 0) for v in self.__vertices]

	def vertices(self):
		return self.__vertices

	def normal(self, point: np.ndarray) -> np.ndarray:
		return self.__normal

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		# See if ray intersects with plane
		plane_collision = self.__plane.ray_intersection(ray)

		if plane_collision is None:
			return None

		intersection = plane_collision.location

		# All vertices are pre-flattened

		# Move all flattened vertices so the intersection is at the origin
		flattened_intersection = np.append(np.delete(intersection, self.__plane_dominant_coord), 0)
		vertices = [v - flattened_intersection for v in self.__flattened_vertices]

		# Make sure no vertices lie on the x-axis
		for v in vertices:
			if v[1] == 0:
				v[1] += 0.00001

		# Not sure what the rest of this algorithm does - I'll revist it later # TODO
		num_crossings = 0

		sign_holder = -1 if vertices[0][1] < 0 else 1

		for i in range(len(vertices)):
			i_1 = i + 1 if i < len(vertices)-1 else 0
			
			next_sign_holder = -1 if vertices[i_1][1] < 0 else 1

			if sign_holder != next_sign_holder:
				if vertices[i][0] > 0 and vertices[i_1][0] > 0:
					# This edge crosses +u'
					num_crossings += 1
				elif vertices[i][0] > 0 or vertices[i_1][0] > 0:
					# The edge might cross +u'
					# Compute the intersection with the u' axis
					u_cross = vertices[i][0] - vertices[i][1] * (vertices[i_1][0] - vertices[i][0]) / (vertices[i_1][1] - vertices[i][1])
					if u_cross > 0:
						# The edge crosses +u
						num_crossings += 1
			
			sign_holder = next_sign_holder

		return Ray_Collision(self, ray, intersection) if num_crossings % 2 == 1 else None
