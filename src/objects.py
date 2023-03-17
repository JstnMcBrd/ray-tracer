import numpy as np

from lib._itertools import closed_pairwise
from ray import Ray, RayCollision
from vector_utils import magnitude, normalized


class Object:
	def __init__(self):
		self.name = ""

		self.ambient_coefficient = 0
		self.diffuse_coefficient = 0
		self.specular_coefficient = 0
		self.diffuse_color = np.array([0, 0, 0])
		self.specular_color = np.array([0, 0, 0])
		self.gloss_coefficient = 0
		self.reflectivity = 0

	def normal(self, point: np.ndarray) -> np.ndarray:
		NotImplemented

	def ray_intersection(self, ray: Ray) -> RayCollision or None:
		NotImplemented


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
		plane_collision = self._plane.ray_intersection(ray)
		if plane_collision is None:
			return None

		# Check if intersection is within circle radius
		intersection = plane_collision.position
		distance = magnitude(intersection - self.center)

		if distance > self.radius:
			return None

		return RayCollision(self, ray, intersection)


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

	def ray_intersection(self, ray: Ray) -> RayCollision or None:
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
		return RayCollision(self, ray, intersection)


class Sphere(Object):
	def __init__(self, center: np.ndarray, radius: float):
		super().__init__()
		self.center = center
		self.radius = radius

	def normal(self, point: np.ndarray) -> np.ndarray:
		return normalized(point - self.center)

	def ray_intersection(self, ray: Ray) -> RayCollision or None:
		dist = self.center - ray.origin
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

		t = closest_approach - closest_approach_dist_to_surface if outside else closest_approach + closest_approach_dist_to_surface

		return RayCollision(self, ray, ray.origin + ray.direction*t)


def triangle_area(v1: np.ndarray, v2: np.ndarray, v3: np.ndarray):
	return abs((v1[0] * (v2[1] - v3[1]) + v2[0] * (v3[1] - v1[1]) + v3[0] * (v1[1] - v2[1])) / 2.0)


class Triangle(Polygon):
	def __init__(self, vertices: list):
		super().__init__(vertices)

		assert len(vertices) == 3, "Triangle must have 3 vertices"

		self._flattened_area = triangle_area(self._flattened_vertices[0], self._flattened_vertices[1], self._flattened_vertices[2])

	def ray_intersection(self, ray: Ray) -> RayCollision or None:
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

		return RayCollision(self, ray, intersection)
