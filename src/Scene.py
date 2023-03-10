import numpy as np

from vector_utils import magnitude, normalized


class Camera:
	def __init__(self, camera_look_at: np.ndarray, camera_look_from: np.ndarray, camera_look_up: np.ndarray, field_of_view: float):
		self.position = camera_look_from
		self.field_of_view = field_of_view

		self.relative_look_at = camera_look_at - camera_look_from
		self.focal_length = magnitude(self.relative_look_at)

		self.forward = normalized(self.relative_look_at)
		self.up = camera_look_up
		self.right = np.cross(self.forward, self.up)


class Scene:
	def __init__(self, camera: Camera, light_direction: np.ndarray, light_color: np.ndarray, ambient_light_color: np.ndarray, background_color: np.ndarray, objects: list):
		# Camera
		self.camera = camera

		# Lighting
		self.light_direction = light_direction
		self.light_color = light_color
		self.ambient_light_color = ambient_light_color
		self.background_color = background_color

		# Objects
		self.objects = objects
