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

class Sphere(Object):
	def __init__(self):
		super().__init__()
		self.center = np.array([0, 0, 0])
		self.radius = 0

	def normal(self, point: np.ndarray) -> np.ndarray:
		if self.radius != 0:
			N = (point - self.center)/self.radius
			return N / np.sqrt(np.dot(N, N)) # Normalize
		else:
			return np.array([0,0,0])

	def ray_intersection(self, ray_origin, ray_direction) -> np.ndarray:
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

# TODO add more types of objects
