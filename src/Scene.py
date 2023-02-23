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

		self.kd = 0
		self.ks = 0
		self.ka = 0
		self.od = np.array([0, 0, 0])
		self.os = np.array([0, 0, 0])
		self.kgls = 0

	def color(self):
		return self.od