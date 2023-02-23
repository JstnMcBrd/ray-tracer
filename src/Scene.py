class Scene:
	def __init__(self):
		self.cameraLookAt = [0.0, 0.0, 0.0]
		self.cameraLookFrom = [0.0, 0.0, 0.0]
		self.cameraLookUp = [0.0, 0.0, 0.0]
		self.fieldOfView = 0
		self.directionToLight = [0, 0, 0]
		self.lightColor = [0, 0, 0]
		self.ambientLightColor = [0, 0, 0]
		self.backgroundColor = [0, 0, 0]
		self.objects = []

class Sphere:
	def __init__(self):
		self.name = ""
		self.center = [0, 0, 0]
		self.radius = 0

		self.kd = 0
		self.ks = 0
		self.ka = 0
		self.od = [0, 0, 0]
		self.os = [0, 0, 0]
		self.kgls = 0