import numpy as np

from ray import Ray, RayCollision

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
