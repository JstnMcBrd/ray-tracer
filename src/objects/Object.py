import numpy as np

class Object:
	def __init__(self):
		self.name = ""

		self.ambient_coefficient = 0
		self.diffuse_coefficient = 0
		self.specular_coefficient = 0
		self.diffuse_color = np.array([0, 0, 0])
		self.specular_color = np.array([0, 0, 0])
		self.gloss_coefficient = 0

	def normal(self, point: np.ndarray) -> np.ndarray:
		NotImplemented

	def ray_intersection(self, ray_origin: np.ndarray, ray_direction: np.ndarray) -> np.ndarray:
		NotImplemented
