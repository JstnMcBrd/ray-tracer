import lib_patches.closed_pairwise
from itertools import closed_pairwise
import numpy as np

from objects.Object import Object
from objects.Plane import Plane
from Ray import Ray, Ray_Collision
from vector_utils import normalized

class Polygon(Object):
	def __init__(self, vertices: list):
		super().__init__()

		assert len(vertices) >= 3, "Polygon must have at least 3 vertices"

		self._vertices = vertices

		v1 = normalized(vertices[1] - vertices[0])
		v2 = normalized(vertices[2] - vertices[1])

		_normal = normalized(np.cross(v1, v2))

		self._plane = Plane(_normal, vertices[0])

		# Project all the vertices onto a 2D plane (for future intersection calculations)
		self._plane_dominant_coord = np.where(np.abs(_normal) == np.max(np.abs(_normal)))[0][0]
		self._flattened_vertices = [np.delete(v, self._plane_dominant_coord) for v in self._vertices]

	def vertices(self):
		return self._vertices

	def normal(self, point: np.ndarray = None) -> np.ndarray:
		return self._plane.normal(point)

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		# See if ray intersects with plane
		plane_collision = self._plane.ray_intersection(ray)
		if plane_collision is None:
			return None
		intersection = plane_collision.position

		# All vertices are pre-flattened in __init__()

		# Move all flattened vertices so the intersection is at the origin
		flattened_intersection = np.delete(intersection, self._plane_dominant_coord)
		vertices = [v - flattened_intersection for v in self._flattened_vertices]

		# Make sure no vertices lie on the x-axis
		for v in vertices:
			if v[1] == 0:
				v[1] += 0.01

		# Calculate how many times polygon edges cross the x-axis
		num_crossings = 0
		for vertex, next_vertex in closed_pairwise(vertices):
			below_x_axis = vertex[1] < 0
			next_below_x_axis = next_vertex[1] < 0

			# If the edge crosses the x axis...
			if below_x_axis != next_below_x_axis:
				right_of_y_axis = vertex[0] > 0
				next_right_of_y_axis = next_vertex[0] > 0

				if right_of_y_axis and next_right_of_y_axis:
					# This edge crosses
					num_crossings += 1
				elif right_of_y_axis or next_right_of_y_axis:
					# The edge might cross
					# Compute intersection with the axis
					vertex_dif = next_vertex - vertex
					cross = vertex[0] - vertex[1] * vertex_dif[0] / vertex_dif[1]

					if cross > 0:
						# The edge crosses
						num_crossings += 1

		# Even number of crossings -> outside polygon -> no collision
		if num_crossings % 2 == 0:
			return None

		# Odd number of crossings -> inside polygon -> yes collision
		return Ray_Collision(self, ray, intersection)
