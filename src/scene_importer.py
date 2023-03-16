"""
Handles importing scenes from JSON files.
"""

from json import loads as json_as_dict
from sys import exit as end_program

import numpy as np

from objects.Circle import Circle
from objects.Object import Object
from objects.Plane import Plane
from objects.Polygon import Polygon
from objects.Sphere import Sphere
from objects.Triangle import Triangle
from scene import Camera, Scene
from vector_utils import magnitude, normalized


def import_scene(file_path: str) -> Scene:
	""" Returns a scene with the values importing from the given file. """

	json_str = None
	try:
		with open(file_path, "r", encoding="utf8") as json_file:
			json_str = json_file.read()
	except OSError as err:
		print(f"\"{file_path}\" is not a valid path\n\t{err}")
		end_program(1)

	json_data = None
	try:
		json_data = json_as_dict(json_str)
	except (ValueError, TypeError) as err:
		print(f"\"{file_path}\" is not a valid json file\n\t{err}")
		end_program(1)

	scene = None
	try:
		scene = __load_from_json(json_data)
	except AssertionError as err:
		print(f"\"{file_path}\" is improperly formatted\n\t{err}")
		end_program(1)

	return scene


def __load_from_json(json: dict) -> Scene:
	""" Imports a scene from a dictionary formatted as a JSON file. """

	error_prefix = "Scene"

	# Camera
	camera_look_at = __validate_position_vector(json.get("camera_look_at"), default=[0,0,0],
					     error_prefix=f"{error_prefix}.camera_look_at")
	camera_look_from = __validate_position_vector(json.get("camera_look_from"), default=[0,0,1],
					       error_prefix=f"{error_prefix}.camera_look_from")
	camera_look_up = __validate_direction_vector(json.get("camera_look_up"), default=[0,1,0],
					      error_prefix=f"{error_prefix}.camera_look_up")
	field_of_view = __validate_number(json.get("field_of_view"), _min=0, _max=359, default=90,
				   error_prefix=f"{error_prefix}.field_of_view")

	camera = Camera(camera_look_at, camera_look_from, camera_look_up, field_of_view)

	# Lighting
	light_direction = __validate_direction_vector(json.get("light_direction"), default=[0,1,0],
					       error_prefix=f"{error_prefix}.light_direction")
	light_color = __validate_color_vector(json.get("light_color"), default=[1,1,1],
				       error_prefix=f"{error_prefix}.light_color")
	ambient_light_color = __validate_color_vector(json.get("ambient_light_color"), default=[1,1,1],
					       error_prefix=f"{error_prefix}.ambient_light_color")
	background_color = __validate_color_vector(json.get("background_color"), default=[0,0,0],
					    error_prefix=f"{error_prefix}.background_color")

	# Objects
	objects = __load_objects(json.get("objects"), default=[], error_prefix=f"{error_prefix}.objects")

	scene = Scene(camera, light_direction, light_color, ambient_light_color, background_color, objects)

	return scene


def __load_objects(json_value, default: list = None, error_prefix="Objects") -> list:
	""" Takes a list of dictionaries and imports each of them as an Object. """

	objects = []

	json_value = __validate_list(json_value, default=default, error_prefix=error_prefix)
	for count, element in enumerate(json_value):
		obj = __load_object(element, error_prefix=f"{error_prefix}[{count}]")
		objects.append(obj)

	return objects


def __load_object(json_value, error_prefix="Object") -> Object:
	""" Imports a dictionary as an Object. """

	obj = None

	assert json_value is not None, f"{error_prefix} must not be missing"
	assert isinstance(json_value, dict), f"{error_prefix} must be type dict, not {type(json_value)}"

	obj_type = json_value.get("type")
	assert obj_type is not None, f"{error_prefix}.type must not be missing"
	assert isinstance(obj_type, str), f"{error_prefix}.type must be type string, not {type(obj_type)}"
	obj_type = obj_type.lower()

	# Load in object-type-specific values
	if obj_type == "circle":
		obj = __load_circle(json_value, error_prefix=f"{error_prefix}<Circle>")
	elif obj_type == "plane":
		obj = __load_plane(json_value, error_prefix=f"{error_prefix}<Plane>")
	elif obj_type == "polygon":
		obj = __load_polygon(json_value, error_prefix=f"{error_prefix}<Polygon>")
	elif obj_type == "sphere":
		obj = __load_sphere(json_value, error_prefix=f"{error_prefix}<Sphere>")
	elif obj_type == "triangle":
		obj = __load_triangle(json_value, error_prefix=f"{error_prefix}<Triangle>")
	else:
		raise f"{error_prefix} must have valid type, not {obj_type}"

	# Load in universal object values
	name = json_value.get("name")
	if name is not None:
		assert isinstance(name, str), f"{error_prefix}.name must be type string, not {type(name)}"
	obj.name = name

	obj.ambient_coefficient = __validate_number(json_value.get("ambient_coefficient"), default=0,
					     error_prefix=f"{error_prefix}.ambient_coefficient")
	obj.diffuse_coefficient = __validate_number(json_value.get("diffuse_coefficient"), default=1,
					     error_prefix=f"{error_prefix}.diffuse_coefficient")
	obj.specular_coefficient = __validate_number(json_value.get("specular_coefficient"), default=0,
					      error_prefix=f"{error_prefix}.specular_coefficient")
	obj.diffuse_color = __validate_color_vector(json_value.get("diffuse_color"), default=[1,1,1],
					     error_prefix=f"{error_prefix}.diffuse_color")
	obj.specular_color = __validate_color_vector(json_value.get("specular_color"), default=[1,1,1],
					      error_prefix=f"{error_prefix}.specular_color")
	obj.gloss_coefficient = __validate_number(json_value.get("gloss_coefficient"), default=4,
					   error_prefix=f"{error_prefix}.gloss_coefficient")
	obj.reflectivity = __validate_number(json_value.get("reflectivity"), default=0,
				      error_prefix=f"{error_prefix}.reflectivity")

	return obj


def __load_circle(json_value, error_prefix="Circle") -> Circle:
	""" Imports Circle-specific values from a dictionary. """

	center = __validate_position_vector(json_value.get("center"), default=[0,0,0],
				     error_prefix=f"{error_prefix}.center")
	radius = __validate_number(json_value.get("radius"), _min=0,
			    error_prefix=f"{error_prefix}.radius")
	normal = __validate_direction_vector(json_value.get("normal"), default=[0,0,1],
				      error_prefix=f"{error_prefix}.normal")

	return Circle(center, radius, normal)


def __load_plane(json_value, error_prefix="Plane") -> Plane:
	""" Imports Plane-specific values from a dictionary. """

	normal = __validate_direction_vector(json_value.get("normal"),
				      error_prefix=f"{error_prefix}.normal")
	point = __validate_position_vector(json_value.get("point"), default=[0,0,0],
				    error_prefix=f"{error_prefix}.point")

	return Plane(normal, point)


def __load_polygon(json_value, error_prefix="Polygon") -> Polygon:
	""" Imports Polygon-specific values from a dictionary. """

	vertices_numpyified = []
	vertices = __validate_list(json_value.get("vertices"), error_prefix=f"{error_prefix}.vertices")

	assert len(vertices) >= 3, f"{error_prefix}.vertices must have at least 3 vertices"

	if len(vertices) == 3:
		print(f"WARNING: {error_prefix} only has 3 vertices, automatically converting to Triangle")
		return __load_triangle(json_value, error_prefix)

	for count, element in enumerate(vertices):
		vertex = __validate_position_vector(element, error_prefix=f"{error_prefix}.vertices[{count}]")
		vertices_numpyified.append(vertex)

	return Polygon(vertices_numpyified)


def __load_sphere(json_value, error_prefix="Sphere") -> Sphere:
	""" Imports Sphere-specific values from a dictionary. """

	center = __validate_position_vector(json_value.get("center"),
				     error_prefix=f"{error_prefix}.center")
	radius = __validate_number(json_value.get("radius"), _min=0,
			    error_prefix=f"{error_prefix}.radius")

	return Sphere(center, radius)


def __load_triangle(json_value, error_prefix="Triangle") -> Triangle:
	""" Imports Triangle-specific values from a dictionary. """

	vertices_numpyified = []
	vertices = __validate_list(json_value.get("vertices"), error_prefix=f"{error_prefix}.vertices")

	assert len(vertices) == 3, f"{error_prefix}.vertices must have 3 vertices"

	for count, element in enumerate(vertices):
		vertex = __validate_position_vector(element, error_prefix=f"{error_prefix}.vertices[{count}]")
		vertices_numpyified.append(vertex)

	return Triangle(vertices_numpyified)


def __validate_position_vector(json_value,
			       default: list = None,
				   error_prefix="Position") -> np.ndarray:
	""" Imports a list as a position vector. """

	json_value = __validate_list(json_value, length=3, default=default, error_prefix=error_prefix)
	for element in json_value:
		__validate_number(element, error_prefix=f"{error_prefix} element")

	return np.array(json_value)


def __validate_direction_vector(json_value,
				default: list = None,
				error_prefix="Direction") -> np.ndarray:
	""" Imports a list as a direction vector, verifying it is normalized. """

	json_value = __validate_list(json_value, length=3, default=default, error_prefix=error_prefix)
	for element in json_value:
		__validate_number(element, error_prefix=f"{error_prefix} element")

	# Convert to numpy array
	vector = np.array(json_value)

	# Make sure the vector is normalized
	mag = magnitude(vector)
	if mag != 1 and mag != 0:
		print(f"WARNING: {error_prefix} is not normalized, performing auto-normalization")
		vector = normalized(vector)
		print(f"WARNING: {error_prefix} has been normalized to [{vector[0]}, {vector[1]}, {vector[2]}]")

	return vector


def __validate_color_vector(json_value,
			    default: list = None,
				error_prefix="Color") -> np.ndarray:
	""" Imports a list as a color vector, verifying the proper range of values. """

	json_value = __validate_list(json_value, length=3, default=default, error_prefix=error_prefix)
	for element in json_value:
		__validate_number(element, _min=0, _max=1, error_prefix=f"{error_prefix} element")

	return np.array(json_value)


def __validate_list(json_value,
		    length: int = None,
			default: list = None,
			error_prefix = "List") -> list:
	""" Imports a list. """

	if json_value is None and default is not None:
		print(f"WARNING: {error_prefix} is missing, reverting to default value {default}")
		return default

	assert json_value is not None, f"{error_prefix} must not be missing"
	assert isinstance(json_value, list), f"{error_prefix} must be type list, not {type(json_value)}"
	if length is not None:
		assert len(json_value) == length, \
			f"{error_prefix} must have {length} elements, not {len(json_value)}"

	return json_value


def __validate_number(json_value,
		      _min: float|int = None,
			  _max: float|int = None,
			  default: float|int = None,
		      error_prefix = "Number") -> float|int:
	""" Imports a number. """

	if json_value is None and default is not None:
		print(f"WARNING: {error_prefix} is missing, reverting to default value {default}")
		return default

	assert json_value is not None, f"{error_prefix} must not be missing"
	assert isinstance(json_value, (float, int)), \
		f"{error_prefix} must be type float or int, not {type(json_value)}"
	if _min is not None:
		assert json_value >= _min, f"{error_prefix} must be greater than {_min}, not {json_value}"
	if _max is not None:
		assert json_value <= _max, f"{error_prefix} must be less than {_max}, not {json_value}"

	return json_value
