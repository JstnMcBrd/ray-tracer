"""
Classes that define the scene to be ray traced.
"""


import numpy as np

from objects import Object
from ray import Ray, RayCollision
from vector import magnitude, normalized


class Camera:
	""" Defines the camera position, orientation, and other settings. """

	def __init__(self, camera_look_at: np.ndarray, camera_look_from: np.ndarray,
			camera_look_up: np.ndarray, field_of_view: float):

		self.position = camera_look_from
		self.field_of_view = field_of_view

		self.relative_look_at = camera_look_at - camera_look_from
		self.focal_length = magnitude(self.relative_look_at)

		self.forward = normalized(self.relative_look_at)
		self.up = camera_look_up
		self.right = np.cross(self.forward, self.up)


class Scene:
	""" Defines the entire scene and all objects within it. """

	def __init__(self, camera: Camera, light_direction: np.ndarray, light_color: np.ndarray,
			ambient_light_color: np.ndarray, background_color: np.ndarray, objects: list[Object]):

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
		""" Projects the ray into the scene and returns the closest object collision. """

		closest_collision: RayCollision | None = None

		# Find the closest object that intersects with the ray
		for obj in self.objects:
			collision = obj.ray_intersection(ray)
			if collision is not None:
				if closest_collision is None or collision.distance < closest_collision.distance:
					closest_collision = collision

		return closest_collision
