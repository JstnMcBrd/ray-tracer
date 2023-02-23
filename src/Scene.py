import numpy as np

class Scene:
	def __init__(self):
		self.cameraLookAt = np.array([0.0, 0.0, 0.0])
		self.cameraLookFrom = np.array([0.0, 0.0, 0.0])
		self.cameraLookUp = np.array([0.0, 0.0, 0.0])
		self.fieldOfView = 0
		self.directionToLight = np.array([0, 0, 0])
		self.lightColor = np.array([0, 0, 0])
		self.ambientLightColor = np.array([0, 0, 0])
		self.backgroundColor = np.array([0, 0, 0])
		self.objects = []

	def cameraForward(self):
		direction = self.cameraLookAt - self.cameraLookFrom
		return direction / np.sqrt(np.dot(direction,direction))

	def cameraUp(self):
		return self.cameraLookUp

	def cameraRight(self):
		return np.cross(self.cameraForward(), self.cameraUp())

class Sphere:
	def __init__(self):
		self.name = ""
		self.center = np.array([0, 0, 0])
		self.radius = 0

		self.ambientCoefficient = 0
		self.diffuseCoefficient = 0
		self.specularCoefficient = 0
		self.diffuseColor = np.array([0, 0, 0])
		self.specularColor = np.array([0, 0, 0])
		self.glossCoefficient = 0

	def normal(self, point: np.ndarray) -> np.ndarray:
		if self.radius != 0:
			N = (point - self.center)/self.radius
			return N / np.sqrt(np.dot(N,N))
		else:
			return np.array([0,0,0])

	def rayIntersection(self, rayOrigin, rayDirection) -> np.ndarray:
		dist = self.center - rayOrigin
		dist_sqr = np.dot(dist, dist)
		dist_mag = np.sqrt(dist_sqr)

		outside = dist_mag >= self.radius

		closestApproach = np.dot(rayDirection, dist)

		if closestApproach < 0 and outside:
			return None

		closestApproachDistToSurface_sqr = self.radius**2 - dist_sqr + closestApproach**2

		if closestApproachDistToSurface_sqr < 0:
			return None
		
		closestApproachDistToSurface = closestApproachDistToSurface_sqr**0.5

		t = closestApproach - closestApproachDistToSurface if outside else closestApproach + closestApproachDistToSurface

		return rayOrigin + rayDirection*t
