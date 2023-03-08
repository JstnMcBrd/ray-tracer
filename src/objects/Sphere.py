import numpy as np

from objects.Object import Object
from vector_utils import normalized

class Sphere(Object):
	def __init__(self, center: np.ndarray, radius: float):
		super().__init__()
		self.center = center
		self.radius = radius

	def normal(self, point: np.ndarray) -> np.ndarray:
		if self.radius != 0:
			N = (point - self.center)/self.radius
			return normalized(N)
		else:
			return np.array([0,0,0])

	def ray_intersection(self, ray_origin, ray_direction) -> np.ndarray or None:
		dist = self.center - ray_origin
		dist_sqr = np.dot(dist, dist)
		dist_mag = np.sqrt(dist_sqr)

		outside = dist_mag >= self.radius

		closest_approach = np.dot(ray_direction, dist)

		if closest_approach < 0 and outside:
			return None

		closest_approach_dist_to_surface_sqr = self.radius**2 - dist_sqr + closest_approach**2

		if closest_approach_dist_to_surface_sqr < 0:
			return None
		
		closest_approach_dist_to_surface = closest_approach_dist_to_surface_sqr**0.5

		t = closest_approach - closest_approach_dist_to_surface if outside else closest_approach + closest_approach_dist_to_surface

		return ray_origin + ray_direction*t
