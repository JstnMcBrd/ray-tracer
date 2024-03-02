"""
Definitions for all supported objects and their behavior.
"""


import numpy as np

from lib._itertools import closed_pairwise
from ray import Ray, RayCollision
from vector import magnitude, normalized


class Object:
	""" The universal values shared by all objects. """

	def __init__(self):
		self.name = ""

		self.ambient_coefficient = 0
		self.diffuse_coefficient = 0
		self.specular_coefficient = 0
		self.diffuse_color = np.array([0, 0, 0])
		self.specular_color = np.array([0, 0, 0])
		self.gloss_coefficient = 0
		self.reflectivity = 0

	# pylint: disable-next=unused-argument
	def normal(self, point: np.ndarray) -> np.ndarray:
		"""
		The "up" direction from this point on the object.
		Assumes the point is actually on the object.
		"""
		return NotImplemented

	# pylint: disable-next=unused-argument
	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		""" Calculates whether the given ray collides with this object. """
		return NotImplemented


class Circle(Object):
	""" The specific values necessary for Circles. """

	def __init__(self, position: np.ndarray, normal: np.ndarray, radius: float):
		super().__init__()

		self.position = position
		self.radius = radius

		normal = normalized(normal)
		self._plane = Plane(position, normal)

	def normal(self, point: np.ndarray | None = None) -> np.ndarray:
		return self._plane.normal(point)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		# See if ray intersects with plane
		plane_collision = self._plane.ray_intersection(ray)
		if plane_collision is None:
			return None

		# Check if intersection is within circle radius
		intersection = plane_collision.position
		distance = magnitude(intersection - self.position)

		if distance > self.radius:
			return None

		return RayCollision(self, ray, intersection)


class Plane(Object):
	""" The specific values necessary for Planes. """

	def __init__(self, position: np.ndarray, normal: np.ndarray):
		super().__init__()

		self._normal = normalized(normal)
		self._distance_from_origin = -1 * np.dot(normal, position)

	def normal(self, point: np.ndarray | None = None) -> np.ndarray:
		return self._normal

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
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


class Polygon(Object):
	""" The specific values necessary for Polygons. """

	def __init__(self, vertices: list):
		super().__init__()

		assert len(vertices) >= 3, "Polygon must have at least 3 vertices"

		self._vertices = vertices

		vector_1 = normalized(vertices[1] - vertices[0])
		vector_2 = normalized(vertices[2] - vertices[1])

		_normal = normalized(np.cross(vector_1, vector_2))

		self._plane = Plane(vertices[0], _normal)

		# Project all the vertices onto a 2D plane (for future intersection calculations)
		self._plane_dominant_coord = np.where(np.abs(_normal) == np.max(np.abs(_normal)))[0][0]
		self._flattened_vertices = [np.delete(v, self._plane_dominant_coord) for v in self._vertices]

	def normal(self, point: np.ndarray | None = None) -> np.ndarray:
		return self._plane.normal(point)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
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
		for vertex in vertices:
			if vertex[1] == 0:
				vertex[1] += 0.01

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
		return RayCollision(self, ray, intersection)


class Sphere(Object):
	""" The specific values necessary for Spheres. """

	def __init__(self, position: np.ndarray, radius: float):
		super().__init__()
		self.position = position
		self.radius = radius

	def normal(self, point: np.ndarray) -> np.ndarray:
		return normalized(point - self.position)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		dist = self.position - ray.origin
		dist_sqr = np.dot(dist, dist)
		dist_mag = np.sqrt(dist_sqr)

		outside = dist_mag >= self.radius

		closest_approach = np.dot(ray.direction, dist)

		if closest_approach < 0 and outside:
			return None

		closest_approach_dist_to_surface_sqr = self.radius**2 - dist_sqr + closest_approach**2

		if closest_approach_dist_to_surface_sqr < 0:
			return None

		closest_approach_dist_to_surface = closest_approach_dist_to_surface_sqr**0.5

		t = closest_approach - closest_approach_dist_to_surface if outside \
			else closest_approach + closest_approach_dist_to_surface

		return RayCollision(self, ray, ray.origin + ray.direction*t)


class Triangle(Polygon):
	"""
	The specific values necessary for Triangles. 
	The algorithm for Triangle intersections is slightly faster than Polygons,
 	so 3-sided Polygons will be automatically converted to Triangles.
	"""

	def __init__(self, vertices: list):
		super().__init__(vertices)

		assert len(vertices) == 3, "Triangle must have 3 vertices"

		self._flattened_area = Triangle.area(self._flattened_vertices)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		# See if ray intersects with plane
		plane_collision = self._plane.ray_intersection(ray)
		if plane_collision is None:
			return None
		intersection = plane_collision.position

		# All vertices are pre-flattened in Polygon.__init__()
		flattened_intersection = np.delete(intersection, self._plane_dominant_coord)

		# Calculate areas
		area_1 = Triangle.area([self._flattened_vertices[0], self._flattened_vertices[1],
			 flattened_intersection])
		area_2 = Triangle.area([self._flattened_vertices[0], self._flattened_vertices[2],
			 flattened_intersection])
		area_3 = Triangle.area([self._flattened_vertices[1], self._flattened_vertices[2],
			 flattened_intersection])

		# If point is inside triangle, then the area of all sub-triangles will add up to the total area
		if abs(area_1 + area_2 + area_3 - self._flattened_area) > 0.0001:
			return None

		return RayCollision(self, ray, intersection)

	@staticmethod
	def area(vertices: list):
		""" Given the three vertices, returns the area of the enclosed triangle. """

		assert len(vertices) == 3, "Must have 3 vertices to be a triangle"

		area = (vertices[0][0] * (vertices[1][1] - vertices[2][1]) \
			+ vertices[1][0] * (vertices[2][1] - vertices[0][1]) \
				+ vertices[2][0] * (vertices[0][1] - vertices[1][1])) / 2.0
		return abs(area)
