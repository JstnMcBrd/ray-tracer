import numpy as np

from objects.Object import Object
from Ray import Ray, Ray_Collision
from vector_utils import normalized

class Sphere(Object):
	def __init__(self, center: np.ndarray, radius: float):
		super().__init__()
		self.center = center
		self.radius = radius

	def normal(self, point: np.ndarray) -> np.ndarray:
		return normalized(point - self.center)

	def ray_intersection(self, ray: Ray) -> Ray_Collision or None:
		dist = self.center - ray.origin
		dist_sqr = np.dot(dist, dist)
		dist_mag = np.sqrt(dist_sqr)

		outside = dist_mag >= self.radius

		closest_approach = np.dot(ray.direction, dist)

		if closest_approach < 0 and outside:
			return None

		closest_approach_dist_to_surface_sqr = self.radius**2 - dist_sqr + closest_approach**2

		if closest_approach_dist_to_surface_sqr < 0:
			return None
		
		closest_approach_dist_to_surface = closest_approach_dist_to_surface_sqr**0.5

		t = closest_approach - closest_approach_dist_to_surface if outside else closest_approach + closest_approach_dist_to_surface

		return Ray_Collision(self, ray, ray.origin + ray.direction*t)
