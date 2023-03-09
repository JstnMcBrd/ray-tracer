import numpy as np

from Ray import Ray, Ray_Collision

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

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		NotImplemented
