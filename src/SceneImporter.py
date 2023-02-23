from Scene import Scene, Sphere

def loadFromJson(json):
	errorPrefix = "Scene"

	scene = Scene()

	scene.cameraLookAt = _validateDirectionVector(json.get("cameraLookAt"), errorPrefix=f"{errorPrefix}.cameraLookAt")
	scene.cameraLookFrom = _validateDirectionVector(json.get("cameraLookFrom"), errorPrefix=f"{errorPrefix}.cameraLookFrom")
	scene.cameraLookUp = _validateDirectionVector(json.get("cameraLookUp"), errorPrefix=f"{errorPrefix}.cameraLookUp")

	# TODO assert cameraLookAt and cameraLookFrom are opposite
	# TODO assert cameraLookUp is perpendicular to cameraLookAt and cameraLookFrom

	scene.fieldOfView = _validateNumber(json.get("fieldOfView"), min=0, max=360, errorPrefix=f"{errorPrefix}.fieldOfView")
	scene.directionToLight = _validateDirectionVector(json.get("directionToLight"), errorPrefix=f"{errorPrefix}.directionToLight")
	scene.lightColor = _validateColorVector(json.get("lightColor"), errorPrefix=f"{errorPrefix}.lightColor")
	scene.ambientLightColor = _validateColorVector(json.get("ambientLightColor"), errorPrefix=f"{errorPrefix}.ambientLightColor")
	scene.backgroundColor = _validateColorVector(json.get("backgroundColor"), errorPrefix=f"{errorPrefix}.backgroundColor")

	scene.objects = _loadObjects(json.get("objects"), errorPrefix=f"{errorPrefix}.objects")

	return scene


def _validateNumber(jsonValue, min=None, max=None, errorPrefix="Number"):
	assert jsonValue != None, f"{errorPrefix} must not be missing"
	assert type(jsonValue) is float or type(jsonValue) is int, f"{errorPrefix} must be type float or int, not {type(jsonValue)}"
	if min != None:
		assert jsonValue >= min, f"{errorPrefix} must be greater than {min}, not {jsonValue}"
	if max != None:
		assert jsonValue <= max, f"{errorPrefix} must be less than {max}, not {jsonValue}"

	return jsonValue


def _validateList(jsonValue, length=None, errorPrefix="List"):
	assert jsonValue != None, f"{errorPrefix} must not be missing"
	assert type(jsonValue) is list, f"{errorPrefix} must be type list, not {type(jsonValue)}"
	if length != None:
		assert len(jsonValue) == length, f"{errorPrefix} must have length of {length}, not {len(jsonValue)}"

	return jsonValue


def _validatePositionVector(jsonValue, errorPrefix="Position"):
	jsonValue = _validateList(jsonValue, length=3, errorPrefix=errorPrefix)
	for i in jsonValue:
		_validateNumber(i, errorPrefix=f"{errorPrefix} element")
		
	return jsonValue


def _validateDirectionVector(jsonValue, errorPrefix="Direction"):
	jsonValue = _validateList(jsonValue, length=3, errorPrefix=errorPrefix)
	for i in jsonValue:
		_validateNumber(i, errorPrefix=f"{errorPrefix} element")

	def vectorLength(v):
		l = 0
		for i in v:
			l += i**2
		return l**0.5
		
	# Normalize vector
	length = vectorLength(jsonValue)
	if length != 1 and length != 0:
		for i in range(len(jsonValue)):
			jsonValue[i] /= length

	length = vectorLength(jsonValue)
	assert length == 1 or length == 0, f"{errorPrefix} must be normalized with length of 0 or 1, not length of {length}"
		
	return jsonValue


def _validateColorVector(jsonValue, errorPrefix="Color"):
	jsonValue = _validateList(jsonValue, length=3, errorPrefix=errorPrefix)
	for i in jsonValue:
		_validateNumber(i, min=0, max=1, errorPrefix=f"{errorPrefix} element")

	return jsonValue


def _loadObjects(jsonValue, errorPrefix="Objects"):
	objects = []

	jsonValue = _validateList(jsonValue, errorPrefix=errorPrefix)
	for i in range(len(jsonValue)):
		obj = _loadObject(jsonValue[i], errorPrefix=f"{errorPrefix}[{i}]")
		objects.append(obj)

	return objects


def _loadObject(jsonValue, errorPrefix="Object"):
	obj = None

	assert jsonValue != None, f"{errorPrefix} must not be missing"
	assert type(jsonValue) is dict, f"{errorPrefix} must be type dict, not {type(jsonValue)}"

	objType = jsonValue.get("type")
	assert objType != None, f"{errorPrefix}.type must not be missing"
	assert type(objType) is str, f"{errorPrefix}.type must be type string, not {type(objType)}"

	# Load in object-type-specific values
	if objType  == "sphere":
		obj = _loadSphere(jsonValue, errorPrefix=f"{errorPrefix}<sphere>")
	# TODO support for more object types later
	else:
		raise f"{errorPrefix} must have valid type, not {objType}"
		
	# Load in universal object values
	name = jsonValue.get("name")
	if name != None:
		assert type(name) is str, f"{errorPrefix}.name must be type string, not {type(name)}"
	obj.name = name

	obj.kd = _validateNumber(jsonValue.get("kd"), errorPrefix=f"{errorPrefix}.kd")
	obj.ks = _validateNumber(jsonValue.get("ks"), errorPrefix=f"{errorPrefix}.ks")
	obj.ka = _validateNumber(jsonValue.get("ka"), errorPrefix=f"{errorPrefix}.ka")
	obj.od = _validateColorVector(jsonValue.get("od"), errorPrefix=f"{errorPrefix}.od")
	obj.os = _validateColorVector(jsonValue.get("os"), errorPrefix=f"{errorPrefix}.os")
	obj.kgls = _validateNumber(jsonValue.get("kgls"), errorPrefix=f"{errorPrefix}.kgls")

	return obj


def _loadSphere(jsonValue, errorPrefix="Sphere"):
	sphere = Sphere()

	sphere.center = _validatePositionVector(jsonValue.get("center"), errorPrefix=f"{errorPrefix}.center")
	sphere.radius = _validateNumber(jsonValue.get("radius"), errorPrefix=f"{errorPrefix}.radius")

	return sphere
