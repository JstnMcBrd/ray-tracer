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

	@staticmethod
	def loadFromJson(json):
		scene = Scene()

		scene.cameraLookAt = Scene.loadDirectionVector(json, "cameraLookAt")
		scene.cameraLookFrom = Scene.loadDirectionVector(json, "cameraLookFrom")
		scene.cameraLookUp = Scene.loadDirectionVector(json, "cameraLookUp")

		# TODO assert cameraLookAt and cameraLookFrom are opposite
		# TODO assert cameraLookUp is perpendicular to cameraLookAt and cameraLookFrom

		scene.fieldOfView = Scene.loadAngleDegrees(json, "fieldOfView")
		scene.directionToLight = Scene.loadDirectionVector(json, "directionToLight")
		scene.lightColor = Scene.loadColorVector(json, "lightColor")
		scene.ambientLightColor = Scene.loadColorVector(json, "ambientLightColor")
		scene.backgroundColor = Scene.loadColorVector(json, "backgroundColor")

		scene.objects = Scene.loadObjects(json, "objects")

		return scene

	@staticmethod
	def loadAngleDegrees(json, name, min=0, max=360):
		angle = json.get(name)

		assert angle != None, f"Scene.{name} is missing"

		assert type(angle) is float or type(angle) is int, f"Scene.{name} must be of type float or int, not {type(angle)}"

		assert angle >= min and angle <= max, f"Scene.${name} must be between {min} and {max}, not {angle}"

		return angle

	@staticmethod
	def loadDirectionVector(json, name):
		vector = json.get(name)

		assert vector != None, f"Scene.{name} is missing"

		assert type(vector) is list, f"Scene.{name} must be of type list, not {type(vector)}"

		assert len(vector) == 3, f"Scene.{name} must have length of 3, not {len(vector)}"

		for i in range(len(vector)):
			assert type(vector[i]) is float or type(vector[i]) is int, f"Scene.{name}[{i}] must be of type float or int, not {type(vector[i])}"
		
		# Normalize vector
		length = (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5
		if length != 0 and length != 1:
			vector[0] /= length
			vector[1] /= length
			vector[2] /= length
		
		length = (vector[0]**2 + vector[1]**2 + vector[2]**2)**0.5
		assert length == 1 or length == 0, f"Scene.{name} must be normalized, but length is {length}"
		
		return vector

	@staticmethod
	def loadColorVector(json, name):
		vector = json.get(name)

		assert vector != None, f"Scene.{name} is missing"

		assert type(vector) is list, f"Scene.{name} must be of type list, not {type(vector)}"

		assert len(vector) == 3, f"Scene.{name} must have length of 3, not {len(vector)}"
		
		for i in range(len(vector)):
			assert type(vector[i]) is float or type(vector[i]) is int, f"Scene.{name}[{i}] must be of type float or int, not {type(vector[i])}"

		for i in range(len(vector)):
			assert vector[i] >= 0 and vector[i] <= 1, f"Scene.{name}[{i}] must be between 0.0 and 1.0, not ${vector[i]}"

		return vector

	@staticmethod
	def loadObjects(json, name):
		parsedObjects = []
		objects = json.get(name)

		assert objects != None, f"Scene.{name} is missing"

		assert type(objects) is list, f"Scene.{name} must be of type list, not {type(vector)}"

		for i in range(len(objects)):
			parsedObj = Scene.loadObject(json, name, i)
			parsedObjects.append(parsedObj)

		return parsedObjects

	@staticmethod
	def loadObject(json, name, index):
		obj = json.get(name)[index]

		assert obj != None, f"Scene.{name}[{index}] must not be undefined"

		assert type(obj) is dict, f"Scene.{name}[{index}] must be of type dictionary, not {type(obj)}"

		# TODO parse into separate objects based on object type

		return obj
