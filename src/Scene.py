import numpy as np

class Scene:
	def __init__(self):
		self.camera_look_at = np.array([0.0, 0.0, 0.0])
		self.camera_look_from = np.array([0.0, 0.0, 0.0])
		self.camera_look_up = np.array([0.0, 0.0, 0.0])
		self.field_of_view = 0
		self.direction_to_light = np.array([0, 0, 0])
		self.light_color = np.array([0, 0, 0])
		self.ambient_light_color = np.array([0, 0, 0])
		self.background_color = np.array([0, 0, 0])
		self.objects = []

	def camera_forward(self):
		direction = self.camera_look_at - self.camera_look_from
		return direction / np.sqrt(np.dot(direction, direction)) # Normalize

	def camera_up(self):
		return self.camera_look_up

	def camera_right(self):
		return np.cross(self.camera_forward(), self.camera_up())
