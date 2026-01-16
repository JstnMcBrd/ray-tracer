"""Definitions for all supported objects and their behavior."""

import numpy as np
from numpy.typing import NDArray

from lib._itertools import closed_pairwise
from ray import Ray, RayCollision
from vector import magnitude, normalized


class Object:
	"""The universal values shared by all objects."""

	name: str | None
	ambient_coefficient: float = 0
	diffuse_coefficient: float = 0
	specular_coefficient: float = 0
	diffuse_color: NDArray[np.float64] = np.array([0, 0, 0])
	specular_color: NDArray[np.float64] = np.array([0, 0, 0])
	gloss_coefficient: float = 0
	reflectivity: float = 0

	def normal(self, point: NDArray[np.float64]) -> NDArray[np.float64]:
		"""
		Return the "up" direction from the point on the object.

		Assumes the point is actually on the object.
		"""
		raise NotImplementedError

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		"""Calculate whether the given ray collides with this object."""
		raise NotImplementedError


class Plane(Object):
	"""The specific values necessary for Planes."""

	_normal: NDArray[np.float64]
	_distance_from_origin: float

	def __init__(
		self, position: NDArray[np.float64], normal: NDArray[np.float64]
	) -> None:
		"""Initialize an instance of Plane."""
		super().__init__()

		self._normal = normalized(normal)
		self._distance_from_origin = -1 * np.dot(normal, position)

	def normal(self, point: NDArray[np.float64] | None = None) -> NDArray[np.float64]:  # noqa: ARG002
		"""Return the "up" direction, which is the same for every point."""
		return self._normal

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		"""Calculate whether the given ray collides with this object."""
		v_d = np.dot(self._normal, ray.direction)
		if v_d == 0:
			# Ray is parallel to plane
			return None

		v_o = -np.dot(self._normal, ray.origin) - self._distance_from_origin
		t = v_o / v_d
		if t <= 0:
			# Intersection point is behind the ray
			return None

		return RayCollision(self, ray, ray.origin + ray.direction * t)


class Circle(Object):
	"""The specific values necessary for Circles."""

	position: NDArray[np.float64]
	radius: float
	_plane: Plane

	def __init__(
		self, position: NDArray[np.float64], normal: NDArray[np.float64], radius: float
	) -> None:
		"""Initialize an instance of Circle."""
		super().__init__()

		self.position = position
		self.radius = radius

		normal = normalized(normal)
		self._plane = Plane(position, normal)

	def normal(self, point: NDArray[np.float64] | None = None) -> NDArray[np.float64]:
		"""Return the "up" direction, which is the same for every point."""
		return self._plane.normal(point)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		"""Calculate whether the given ray collides with this object."""
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


class Polygon(Object):
	"""The specific values necessary for Polygons."""

	MIN_VERTICES = 3

	X_AXIS_SHIFT = 0.01
	"To make sure no flattened relative vertices lie on the x-axis."

	_vertices: list[NDArray[np.float64]]
	_plane: Plane
	_plane_dominant_coord: int
	_flattened_vertices: list[NDArray[np.float64]]

	def __init__(self, vertices: list[NDArray[np.float64]]) -> None:
		"""Initialize an instance of Polygon."""
		super().__init__()

		if len(vertices) < Polygon.MIN_VERTICES:
			raise ValueError("Polygon must have at least 3 vertices")

		self._vertices = vertices

		vector_1 = normalized(vertices[1] - vertices[0])
		vector_2 = normalized(vertices[2] - vertices[1])

		_normal = normalized(np.cross(vector_1, vector_2))
		self._plane = Plane(self._vertices[0], _normal)

		# Project all the vertices onto a 2D plane for future intersection calculations
		self._plane_dominant_coord: int = np.where(
			np.abs(_normal) == np.max(np.abs(_normal)),
		)[0][0]
		self._flattened_vertices = [
			np.delete(v, self._plane_dominant_coord) for v in self._vertices
		]

	def normal(self, point: NDArray[np.float64] | None = None) -> NDArray[np.float64]:
		"""Return the "up" direction, which is the same for every point."""
		return self._plane.normal(point)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		"""Calculate whether the given ray collides with this object."""
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
				vertex[1] += Polygon.X_AXIS_SHIFT

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


class Triangle(Polygon):
	"""
	The specific values necessary for Triangles.

	The algorithm for Triangle intersections is slightly faster than Polygons,
	so 3-sided Polygons will be automatically converted to Triangles.
	"""

	REQUIRED_VERTICES = 3

	TOLERANCE = 0.0001
	"Tolerance for floating-point area calculations."

	_flattened_area: float

	def __init__(self, vertices: list[NDArray[np.float64]]) -> None:
		"""Initialize an instance of Triangle."""
		super().__init__(vertices)

		if len(vertices) != Triangle.REQUIRED_VERTICES:
			raise ValueError(
				f"Triangle must have {Triangle.REQUIRED_VERTICES} vertices"
			)

		self._flattened_area = Triangle.area(self._flattened_vertices)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		"""Calculate whether the given ray collides with this object."""
		# See if ray intersects with plane
		plane_collision = self._plane.ray_intersection(ray)
		if plane_collision is None:
			return None
		intersection = plane_collision.position

		# All vertices are pre-flattened in Polygon.__init__()
		flattened_intersection = np.delete(intersection, self._plane_dominant_coord)

		# Calculate areas
		area_1 = Triangle.area(
			[
				self._flattened_vertices[0],
				self._flattened_vertices[1],
				flattened_intersection,
			]
		)
		area_2 = Triangle.area(
			[
				self._flattened_vertices[0],
				self._flattened_vertices[2],
				flattened_intersection,
			]
		)
		area_3 = Triangle.area(
			[
				self._flattened_vertices[1],
				self._flattened_vertices[2],
				flattened_intersection,
			]
		)

		# If point is inside triangle, then the area of all sub-triangles
		# will add up to the total area
		if abs(area_1 + area_2 + area_3 - self._flattened_area) > Triangle.TOLERANCE:
			return None

		return RayCollision(self, ray, intersection)

	@staticmethod
	def area(vertices: list[NDArray[np.float64]]) -> float:
		"""Given the three vertices, return the area of the enclosed triangle."""
		if len(vertices) != Triangle.REQUIRED_VERTICES:
			raise ValueError(
				f"Triangle must have \
				{Triangle.REQUIRED_VERTICES} vertices"
			)

		area: float = (
			vertices[0][0] * (vertices[1][1] - vertices[2][1])
			+ vertices[1][0] * (vertices[2][1] - vertices[0][1])
			+ vertices[2][0] * (vertices[0][1] - vertices[1][1])
		) / 2.0
		return abs(area)


class Sphere(Object):
	"""The specific values necessary for Spheres."""

	position: NDArray[np.float64]
	radius: float

	def __init__(self, position: NDArray[np.float64], radius: float) -> None:
		"""Initialize an instance of Sphere."""
		super().__init__()
		self.position = position
		self.radius = radius

	def normal(self, point: NDArray[np.float64]) -> NDArray[np.float64]:
		"""Return the "up" direction from the point on the object."""
		return normalized(point - self.position)

	def ray_intersection(self, ray: Ray) -> RayCollision | None:
		"""Calculate whether the given ray collides with this object."""
		relative_position = self.position - ray.origin
		distance_sqr = np.dot(relative_position, relative_position)
		distance = distance_sqr**0.5

		origin_outside = distance >= self.radius

		closest_approach = np.dot(ray.direction, relative_position)

		if closest_approach < 0 and origin_outside:
			return None

		closest_approach_dist_to_surface_sqr = (
			self.radius**2 - distance_sqr + closest_approach**2
		)

		if closest_approach_dist_to_surface_sqr < 0:
			return None

		closest_approach_dist_to_surface = closest_approach_dist_to_surface_sqr**0.5

		t = (
			(closest_approach - closest_approach_dist_to_surface)
			if origin_outside
			else (closest_approach + closest_approach_dist_to_surface)
		)

		return RayCollision(self, ray, ray.origin + ray.direction * t)
