from json import loads as json_as_dict
import numpy as np

from objects.Circle import Circle
from objects.Object import Object
from objects.Plane import Plane
from objects.Polygon import Polygon
from objects.Sphere import Sphere
from objects.Triangle import Triangle
from Scene import Camera, Scene
from vector_utils import magnitude, normalized

def import_scene(file_path: str) -> Scene:
	json_str = None
	try:
		json_str = open(file_path, "r").read()
	except Exception as err:
		print(f"\"{file_path}\" is not a valid path\n\t{err}")
		exit(1)

	json_data = None
	try:
		json_data = json_as_dict(json_str)
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

	# Camera
	camera_look_at = __validate_position_vector(json.get("camera_look_at"), default=[0,0,0], error_prefix=f"{error_prefix}.camera_look_at")
	camera_look_from = __validate_position_vector(json.get("camera_look_from"), default=[0,0,1], error_prefix=f"{error_prefix}.camera_look_from")
	camera_look_up = __validate_direction_vector(json.get("camera_look_up"), default=[0,1,0], error_prefix=f"{error_prefix}.camera_look_up")
	# TODO assert camera_look_up is perpendicular to the normalized difference between camera_look_at and camera_look_from
	field_of_view = __validate_number(json.get("field_of_view"), min=0, max=359, default=90, error_prefix=f"{error_prefix}.field_of_view")
	
	camera = Camera(camera_look_at, camera_look_from, camera_look_up, field_of_view)

	# Lighting
	light_direction = __validate_direction_vector(json.get("light_direction"), default=[0,1,0], error_prefix=f"{error_prefix}.light_direction")
	light_color = __validate_color_vector(json.get("light_color"), default=[1,1,1], error_prefix=f"{error_prefix}.light_color")
	ambient_light_color = __validate_color_vector(json.get("ambient_light_color"), default=[1,1,1], error_prefix=f"{error_prefix}.ambient_light_color")
	background_color = __validate_color_vector(json.get("background_color"), default=[0,0,0], error_prefix=f"{error_prefix}.background_color")

	# Objects
	objects = __load_objects(json.get("objects"), default=[], error_prefix=f"{error_prefix}.objects")

	scene = Scene(camera, light_direction, light_color, ambient_light_color, background_color, objects)

	return scene


def __load_objects(json_value, default=None, error_prefix="Objects") -> list:
	objects = []

	json_value = __validate_list(json_value, default=default, error_prefix=error_prefix)
	for i in range(len(json_value)):
		obj = __load_object(json_value[i], error_prefix=f"{error_prefix}[{i}]")
		objects.append(obj)

	return objects


def __load_object(json_value, error_prefix="Object") -> Object:
	obj = None

	assert json_value is not None, f"{error_prefix} must not be missing"
	assert type(json_value) is dict, f"{error_prefix} must be type dict, not {type(json_value)}"

	objType = json_value.get("type")
	assert objType is not None, f"{error_prefix}.type must not be missing"
	assert type(objType) is str, f"{error_prefix}.type must be type string, not {type(objType)}"
	objType = objType.lower()

	# Load in object-type-specific values
	if objType == "circle":
		obj = __load_circle(json_value, error_prefix=f"{error_prefix}<Circle>")
	elif objType == "plane":
		obj = __load_plane(json_value, error_prefix=f"{error_prefix}<Plane>")
	elif objType == "polygon":
		obj = __load_polygon(json_value, error_prefix=f"{error_prefix}<Polygon>")
	elif objType == "sphere":
		obj = __load_sphere(json_value, error_prefix=f"{error_prefix}<Sphere>")
	elif objType == "triangle":
		obj = __load_triangle(json_value, error_prefix=f"{error_prefix}<Triangle>")
	# TODO support for more object types
	else:
		raise f"{error_prefix} must have valid type, not {objType}"
		
	# Load in universal object values
	name = json_value.get("name")
	if name is not None:
		assert type(name) is str, f"{error_prefix}.name must be type string, not {type(name)}"
	obj.name = name

	obj.ambient_coefficient = __validate_number(json_value.get("ambient_coefficient"), default=0, error_prefix=f"{error_prefix}.ambient_coefficient")
	obj.diffuse_coefficient = __validate_number(json_value.get("diffuse_coefficient"), default=1, error_prefix=f"{error_prefix}.diffuse_coefficient")
	obj.specular_coefficient = __validate_number(json_value.get("specular_coefficient"), default=0, error_prefix=f"{error_prefix}.specular_coefficient")
	obj.diffuse_color = __validate_color_vector(json_value.get("diffuse_color"), default=[1,1,1], error_prefix=f"{error_prefix}.diffuse_color")
	obj.specular_color = __validate_color_vector(json_value.get("specular_color"), default=[1,1,1], error_prefix=f"{error_prefix}.specular_color")
	obj.gloss_coefficient = __validate_number(json_value.get("gloss_coefficient"), default=4, error_prefix=f"{error_prefix}.gloss_coefficient")
	obj.reflectivity = __validate_number(json_value.get("reflectivity"), default=0, error_prefix=f"{error_prefix}.reflectivity")

	return obj


def __load_circle(json_value, error_prefix="Circle") -> Circle:
	center = __validate_position_vector(json_value.get("center"), default=[0,0,0], error_prefix=f"{error_prefix}.center")
	radius = __validate_number(json_value.get("radius"), min=0, error_prefix=f"{error_prefix}.radius")
	normal = __validate_direction_vector(json_value.get("normal"), default=[0,0,1], error_prefix=f"{error_prefix}.normal")

	return Circle(center, radius, normal)


def __load_plane(json_value, error_prefix="Plane") -> Plane:
	normal = __validate_direction_vector(json_value.get("normal"), error_prefix=f"{error_prefix}.normal")
	point = __validate_position_vector(json_value.get("point"), default=[0,0,0], error_prefix=f"{error_prefix}.point")

	return Plane(normal, point)


def __load_polygon(json_value, error_prefix="Polygon") -> Polygon:
	vertices_numpyified = []
	vertices = __validate_list(json_value.get("vertices"), error_prefix=f"{error_prefix}.vertices")

	assert len(vertices) >= 3, f"{error_prefix}.vertices must have at least 3 vertices"

	if len(vertices) == 3:
		print(f"WARNING: {error_prefix} only has 3 vertices, automatically converting to Triangle")
		return __load_triangle(json_value, error_prefix)

	for i in range(len(vertices)):
		vertex = __validate_position_vector(vertices[i], error_prefix=f"{error_prefix}.vertices[{i}]")
		vertices_numpyified.append(vertex)
	
	return Polygon(vertices_numpyified)


def __load_sphere(json_value, error_prefix="Sphere") -> Sphere:
	center = __validate_position_vector(json_value.get("center"), error_prefix=f"{error_prefix}.center")
	radius = __validate_number(json_value.get("radius"), min=0, error_prefix=f"{error_prefix}.radius")

	return Sphere(center, radius)


def __load_triangle(json_value, error_prefix="Triangle") -> Triangle:
	vertices_numpyified = []
	vertices = __validate_list(json_value.get("vertices"), error_prefix=f"{error_prefix}.vertices")

	assert len(vertices) == 3, f"{error_prefix}.vertices must have 3 vertices"

	for i in range(len(vertices)):
		vertex = __validate_position_vector(vertices[i], error_prefix=f"{error_prefix}.vertices[{i}]")
		vertices_numpyified.append(vertex)
	
	return Triangle(vertices_numpyified)


def __validate_number(json_value, min=None, max=None, default=None, error_prefix="Number") -> float or int:
	if json_value is None and default is not None:
		print(f"WARNING: {error_prefix} is missing, reverting to default value {default}")
		return default

	assert json_value is not None, f"{error_prefix} must not be missing"
	assert type(json_value) is float or type(json_value) is int, f"{error_prefix} must be type float or int, not {type(json_value)}"
	if min is not None:
		assert json_value >= min, f"{error_prefix} must be greater than {min}, not {json_value}"
	if max is not None:
		assert json_value <= max, f"{error_prefix} must be less than {max}, not {json_value}"

	return json_value


def __validate_list(json_value, length=None, default=None, error_prefix="List") -> list:
	if json_value is None and default is not None:
		print(f"WARNING: {error_prefix} is missing, reverting to default value {default}")
		return default

	assert json_value is not None, f"{error_prefix} must not be missing"
	assert type(json_value) is list, f"{error_prefix} must be type list, not {type(json_value)}"
	if length is not None:
		assert len(json_value) == length, f"{error_prefix} must have length of {length}, not {len(json_value)}"

	return json_value


def __validate_position_vector(json_value, default=None, error_prefix="Position") -> np.ndarray:
	json_value = __validate_list(json_value, length=3, default=default, error_prefix=error_prefix)
	for i in json_value:
		__validate_number(i, error_prefix=f"{error_prefix} element")
		
	return np.array(json_value)


def __validate_direction_vector(json_value, default=None, error_prefix="Direction") -> np.ndarray:
	json_value = __validate_list(json_value, length=3, default=default, error_prefix=error_prefix)
	for i in json_value:
		__validate_number(i, error_prefix=f"{error_prefix} element")
		
	# Convert to numpy array
	vector = np.array(json_value)

	# Make sure the vector is normalized
	mag = magnitude(vector)
	if mag != 1 and mag != 0:
		print(f"WARNING: {error_prefix} is not normalized with magnitude of {mag}, performing auto-normalization")
		vector = normalized(vector)
		print(f"WARNING: {error_prefix} has been normalized to [{vector[0]}, {vector[1]}, {vector[2]}]")
		
	return vector


def __validate_color_vector(json_value, default=None, error_prefix="Color") -> np.ndarray:
	json_value = __validate_list(json_value, length=3, default=default, error_prefix=error_prefix)
	for i in json_value:
		__validate_number(i, min=0, max=1, error_prefix=f"{error_prefix} element")

	return np.array(json_value)
