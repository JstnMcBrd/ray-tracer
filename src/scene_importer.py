import json
import numpy as np

from objects.Object import Object
from objects.Sphere import Sphere
from Scene import Scene

def import_scene(file_path: str) -> Scene:
	json_file = None
	try:
		json_file = open(file_path, "r")
	except Exception as err:
		print(f"\"{file_path}\" is not a valid path\n\t{err}")
		exit(1)

	json_data = None
	try:
		json_data = json.loads(json_file.read())
	except Exception as err:
		print(f"\"{file_path}\" is not a valid json file\n\t{err}")
		exit(1)

	scene = None
	try:
		scene = __load_from_json(json_data)
	except AssertionError as err:
		print(f"\"{file_path}\" is improperly formatted\n\t{err}")
		exit(1)

	return scene


def __load_from_json(json) -> Scene:
	error_prefix = "Scene"

	scene = Scene()

	scene.camera_look_at = __validate_direction_vector(json.get("camera_look_at"), error_prefix=f"{error_prefix}.camera_look_at")
	scene.camera_look_from = __validate_position_vector(json.get("camera_look_from"), error_prefix=f"{error_prefix}.camera_look_from")
	scene.camera_look_up = __validate_direction_vector(json.get("camera_look_up"), error_prefix=f"{error_prefix}.camera_look_up")

	# TODO assert camera_look_up is perpendicular to the normalized difference between camera_look_at and camera_look_from

	scene.field_of_view = __validate_number(json.get("field_of_view"), min=0, max=360, error_prefix=f"{error_prefix}.field_of_view")
	scene.direction_to_light = __validate_direction_vector(json.get("direction_to_light"), error_prefix=f"{error_prefix}.direction_to_light")
	scene.light_color = __validate_color_vector(json.get("light_color"), error_prefix=f"{error_prefix}.light_color")
	scene.ambient_light_color = __validate_color_vector(json.get("ambient_light_color"), error_prefix=f"{error_prefix}.ambient_light_color")
	scene.background_color = __validate_color_vector(json.get("background_color"), error_prefix=f"{error_prefix}.background_color")

	scene.objects = __load_objects(json.get("objects"), error_prefix=f"{error_prefix}.objects")

	return scene


def __validate_number(json_value, min=None, max=None, error_prefix="Number") -> float|int:
	assert json_value != None, f"{error_prefix} must not be missing"
	assert type(json_value) is float or type(json_value) is int, f"{error_prefix} must be type float or int, not {type(json_value)}"
	if min != None:
		assert json_value >= min, f"{error_prefix} must be greater than {min}, not {json_value}"
	if max != None:
		assert json_value <= max, f"{error_prefix} must be less than {max}, not {json_value}"

	return json_value


def __validate_list(json_value, length=None, error_prefix="List") -> list:
	assert json_value != None, f"{error_prefix} must not be missing"
	assert type(json_value) is list, f"{error_prefix} must be type list, not {type(json_value)}"
	if length != None:
		assert len(json_value) == length, f"{error_prefix} must have length of {length}, not {len(json_value)}"

	return json_value


def __validate_position_vector(json_value, error_prefix="Position") -> np.ndarray:
	json_value = __validate_list(json_value, length=3, error_prefix=error_prefix)
	for i in json_value:
		__validate_number(i, error_prefix=f"{error_prefix} element")
		
	return np.array(json_value)


def __validate_direction_vector(json_value, error_prefix="Direction") -> np.ndarray:
	json_value = __validate_list(json_value, length=3, error_prefix=error_prefix)
	for i in json_value:
		__validate_number(i, error_prefix=f"{error_prefix} element")

	def vector_magnitude(v):
		l = 0
		for i in v:
			l += i**2
		return l**0.5
		
	# Normalize vector
	mag = vector_magnitude(json_value)
	if mag != 1 and mag != 0:
		for i in range(len(json_value)):
			json_value[i] /= mag

	mag = vector_magnitude(json_value)
	assert mag == 1 or mag == 0, f"{error_prefix} must be normalized with magnitude of 0 or 1, not magnitude of {mag}"
		
	return np.array(json_value)


def __validate_color_vector(json_value, error_prefix="Color") -> np.ndarray:
	json_value = __validate_list(json_value, length=3, error_prefix=error_prefix)
	for i in json_value:
		__validate_number(i, min=0, max=1, error_prefix=f"{error_prefix} element")

	return np.array(json_value)


def __load_objects(json_value, error_prefix="Objects") -> list:
	objects = []

	json_value = __validate_list(json_value, error_prefix=error_prefix)
	for i in range(len(json_value)):
		obj = __load_object(json_value[i], error_prefix=f"{error_prefix}[{i}]")
		objects.append(obj)

	return objects


def __load_object(json_value, error_prefix="Object") -> Object:
	obj = None

	assert json_value != None, f"{error_prefix} must not be missing"
	assert type(json_value) is dict, f"{error_prefix} must be type dict, not {type(json_value)}"

	objType = json_value.get("type")
	assert objType != None, f"{error_prefix}.type must not be missing"
	assert type(objType) is str, f"{error_prefix}.type must be type string, not {type(objType)}"

	# Load in object-type-specific values
	if objType  == "sphere":
		obj = _loadSphere(json_value, error_prefix=f"{error_prefix}<sphere>")
	# TODO support for more object types later
	else:
		raise f"{error_prefix} must have valid type, not {objType}"
		
	# Load in universal object values
	name = json_value.get("name")
	if name != None:
		assert type(name) is str, f"{error_prefix}.name must be type string, not {type(name)}"
	obj.name = name

	obj.ambient_coefficient = __validate_number(json_value.get("ambient_coefficient"), error_prefix=f"{error_prefix}.ambient_coefficient")
	obj.diffuse_coefficient = __validate_number(json_value.get("diffuse_coefficient"), error_prefix=f"{error_prefix}.diffuse_coefficient")
	obj.specular_coefficient = __validate_number(json_value.get("specular_coefficient"), error_prefix=f"{error_prefix}.specular_coefficient")
	obj.diffuse_color = __validate_color_vector(json_value.get("diffuse_color"), error_prefix=f"{error_prefix}.diffuse_color")
	obj.specular_color = __validate_color_vector(json_value.get("specular_color"), error_prefix=f"{error_prefix}.specular_color")
	obj.gloss_coefficient = __validate_number(json_value.get("gloss_coefficient"), error_prefix=f"{error_prefix}.gloss_coefficient")

	return obj


def _loadSphere(json_value, error_prefix="Sphere") -> Sphere:
	sphere = Sphere()

	sphere.center = __validate_position_vector(json_value.get("center"), error_prefix=f"{error_prefix}.center")
	sphere.radius = __validate_number(json_value.get("radius"), error_prefix=f"{error_prefix}.radius")

	return sphere
