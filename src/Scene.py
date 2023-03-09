import numpy as np

from vector_utils import normalized

class Scene:
	def __init__(self):
		# Camera
		self.camera_look_at = np.array([0.0, 0.0, 0.0])
		self.camera_look_from = np.array([0.0, 0.0, 0.0])
		self.camera_look_up = np.array([0.0, 0.0, 0.0])
		self.field_of_view = 0

		# Lighting
		self.light_direction = np.array([0, 0, 0])
		self.light_color = np.array([0, 0, 0])
		self.ambient_light_color = np.array([0, 0, 0])
		self.background_color = np.array([0, 0, 0])

		# Objects
		self.objects = []

	# Call this whenever camera_look_at, camera_look_from, or camera_look_up are updated
	def update_camera_axes(self):
		self.camera_look_at_relative = self.camera_look_at - self.camera_look_from

		self.camera_forward = normalized(self.camera_look_at_relative)

		self.camera_up = self.camera_look_up

		self.camera_right = np.cross(self.camera_forward, self.camera_up)
