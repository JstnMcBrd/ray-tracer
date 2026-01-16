"""Classes that define the scene to be ray traced."""

import numpy as np
from numpy.typing import NDArray

from objects import Object
from ray import Ray, RayCollision
from vector import magnitude, normalized


class Camera:
	"""Defines the camera position, orientation, and other settings."""

	position: NDArray[np.float64]
	field_of_view: float
	relative_look_at: NDArray[np.float64]
	focal_length: float
	forward: NDArray[np.floating]
	up: NDArray[np.floating]
	right: NDArray[np.floating]

	def __init__(
		self,
		camera_look_at: NDArray[np.float64],
		camera_look_from: NDArray[np.float64],
		camera_look_up: NDArray[np.float64],
		field_of_view: float,
	) -> None:
		"""Initialize an instance of Camera."""
		self.position = camera_look_from
		self.field_of_view = field_of_view

		self.relative_look_at = camera_look_at - camera_look_from
		self.focal_length = magnitude(self.relative_look_at)

		self.forward = normalized(self.relative_look_at)
		self.up = camera_look_up
		self.right = np.cross(self.forward, self.up)


class Scene:
	"""Defines the entire scene and all objects within it."""

	camera: Camera
	light_direction: NDArray[np.float64]
	light_color: NDArray[np.float64]
	ambient_light_color: NDArray[np.float64]
	background_color: NDArray[np.float64]
	objects: list[Object]

	def __init__(
		self,
		camera: Camera,
		light_direction: NDArray[np.float64],
		light_color: NDArray[np.float64],
		ambient_light_color: NDArray[np.float64],
		background_color: NDArray[np.float64],
		objects: list[Object],
	) -> None:
		"""Initialize an instance of Scene."""
		# Camera
		self.camera = camera

		# Lighting
		self.light_direction = light_direction
		self.light_color = light_color
		self.ambient_light_color = ambient_light_color
		self.background_color = background_color

		# Objects
		self.objects = objects

	def cast_ray(self, ray: Ray) -> RayCollision | None:
		"""Projects the ray into the scene and returns the closest object collision."""
		collisions = [obj.ray_intersection(ray) for obj in self.objects]
		real = list(filter(None, collisions))
		return min(real, key=lambda c: c.distance) if real else None
