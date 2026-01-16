"""Handles importing scenes from JSON files."""

import sys
from json import loads as json_as_dict
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from objects import Circle, Object, Plane, Polygon, Sphere, Triangle
from scene import Camera, Scene
from vector import magnitude, normalized


def import_scene(file_path: str) -> Scene:
	"""Return a scene with the values importing from the given file."""
	json_str = None
	try:
		with Path(file_path).open(encoding="utf8") as json_file:
			json_str = json_file.read()
	except OSError as err:
		print(f'"{file_path}" is not a valid path\n\t{err}')
		sys.exit(1)

	json_data: dict
	try:
		json_data = json_as_dict(json_str)
	except (TypeError, ValueError) as err:
		print(f'"{file_path}" is not a valid json file\n\t{err}')
		sys.exit(1)

	scene: Scene
	try:
		scene = _load_from_json(json_data)
	except (TypeError, ValueError) as err:
		print(f'"{file_path}" is improperly formatted\n\t{err}')
		sys.exit(1)

	return scene


def _load_from_json(json: dict) -> Scene:
	"""Import a scene from a dictionary formatted as a JSON file."""
	error_prefix = "Scene"

	# Camera
	camera_look_at = _validate_position_vector(
		json.get("camera_look_at"),
		default=[0, 0, 0],
		error_prefix=f"{error_prefix}.camera_look_at",
	)
	camera_look_from = _validate_position_vector(
		json.get("camera_look_from"),
		default=[0, 0, 1],
		error_prefix=f"{error_prefix}.camera_look_from",
	)
	camera_look_up = _validate_direction_vector(
		json.get("camera_look_up"),
		default=[0, 1, 0],
		error_prefix=f"{error_prefix}.camera_look_up",
	)
	field_of_view = _validate_number(
		json.get("field_of_view"),
		_min=0,
		_max=359,
		default=90,
		error_prefix=f"{error_prefix}.field_of_view",
	)

	camera = Camera(camera_look_at, camera_look_from, camera_look_up, field_of_view)

	# Lighting
	light_direction = _validate_direction_vector(
		json.get("light_direction"),
		default=[0, 1, 0],
		error_prefix=f"{error_prefix}.light_direction",
	)
	light_color = _validate_color_vector(
		json.get("light_color"),
		default=[1, 1, 1],
		error_prefix=f"{error_prefix}.light_color",
	)
	ambient_light_color = _validate_color_vector(
		json.get("ambient_light_color"),
		default=[1, 1, 1],
		error_prefix=f"{error_prefix}.ambient_light_color",
	)
	background_color = _validate_color_vector(
		json.get("background_color"),
		default=[0, 0, 0],
		error_prefix=f"{error_prefix}.background_color",
	)

	# Objects
	objects = _load_objects(
		json.get("objects"),
		default=[],
		error_prefix=f"{error_prefix}.objects",
	)

	return Scene(
		camera,
		light_direction,
		light_color,
		ambient_light_color,
		background_color,
		objects,
	)


def _load_objects(
	json_value: Any | None,
	default: list[Object] | None = None,
	error_prefix: str = "Objects",
) -> list[Object]:
	"""Take a list of dictionaries and imports each of them as an Object."""
	objects = []

	json_value = _validate_list(json_value, default=default, error_prefix=error_prefix)
	for count, element in enumerate(json_value):
		obj = _load_object(element, error_prefix=f"{error_prefix}[{count}]")
		objects.append(obj)

	return objects


def _load_object(json_value: Any | None, error_prefix: str = "Object") -> Object:
	"""Import a dictionary as an Object."""
	obj: Object | None = None

	if json_value is None:
		raise ValueError(f"{error_prefix} must not be missing")
	if not isinstance(json_value, dict):
		raise TypeError(f"{error_prefix} must be type dict, not {type(json_value)}")

	obj_type = json_value.get("type")
	if obj_type is None:
		raise ValueError(f"{error_prefix}.type must not be missing")
	if not isinstance(obj_type, str):
		raise TypeError(
			f"{error_prefix}.type must be type string, not {type(obj_type)}"
		)
	obj_type = obj_type.lower()

	# Load in object-type-specific values
	if obj_type == "circle":
		obj = _load_circle(json_value, error_prefix=f"{error_prefix}<Circle>")
	elif obj_type == "plane":
		obj = _load_plane(json_value, error_prefix=f"{error_prefix}<Plane>")
	elif obj_type == "polygon":
		obj = _load_polygon(json_value, error_prefix=f"{error_prefix}<Polygon>")
	elif obj_type == "sphere":
		obj = _load_sphere(json_value, error_prefix=f"{error_prefix}<Sphere>")
	elif obj_type == "triangle":
		obj = _load_triangle(json_value, error_prefix=f"{error_prefix}<Triangle>")
	else:
		raise TypeError(f"{error_prefix} must have valid type, not {obj_type}")

	# Load in universal object values
	name = json_value.get("name")
	if name is not None and not isinstance(name, str):
		raise TypeError(f"{error_prefix}.name must be type string, not {type(name)}")
	obj.name = name

	obj.ambient_coefficient = _validate_number(
		json_value.get("ambient_coefficient"),
		default=0,
		error_prefix=f"{error_prefix}.ambient_coefficient",
	)
	obj.diffuse_coefficient = _validate_number(
		json_value.get("diffuse_coefficient"),
		default=1,
		error_prefix=f"{error_prefix}.diffuse_coefficient",
	)
	obj.specular_coefficient = _validate_number(
		json_value.get("specular_coefficient"),
		default=0,
		error_prefix=f"{error_prefix}.specular_coefficient",
	)
	obj.diffuse_color = _validate_color_vector(
		json_value.get("diffuse_color"),
		default=[1, 1, 1],
		error_prefix=f"{error_prefix}.diffuse_color",
	)
	obj.specular_color = _validate_color_vector(
		json_value.get("specular_color"),
		default=[1, 1, 1],
		error_prefix=f"{error_prefix}.specular_color",
	)
	obj.gloss_coefficient = _validate_number(
		json_value.get("gloss_coefficient"),
		default=4,
		error_prefix=f"{error_prefix}.gloss_coefficient",
	)
	obj.reflectivity = _validate_number(
		json_value.get("reflectivity"),
		default=0,
		error_prefix=f"{error_prefix}.reflectivity",
	)

	return obj


def _load_plane(json_value: dict, error_prefix: str = "Plane") -> Plane:
	"""Import Plane-specific values from a dictionary."""
	position = _validate_position_vector(
		json_value.get("position"),
		default=[0, 0, 0],
		error_prefix=f"{error_prefix}.position",
	)
	normal = _validate_direction_vector(
		json_value.get("normal"),
		error_prefix=f"{error_prefix}.normal",
	)

	return Plane(position, normal)


def _load_circle(json_value: dict, error_prefix: str = "Circle") -> Circle:
	"""Import Circle-specific values from a dictionary."""
	position = _validate_position_vector(
		json_value.get("position"),
		error_prefix=f"{error_prefix}.position",
	)
	normal = _validate_direction_vector(
		json_value.get("normal"),
		default=[0, 0, 1],
		error_prefix=f"{error_prefix}.normal",
	)
	radius = _validate_number(
		json_value.get("radius"),
		_min=0,
		error_prefix=f"{error_prefix}.radius",
	)

	return Circle(position, normal, radius)


def _load_polygon(json_value: dict, error_prefix: str = "Polygon") -> Polygon:
	"""Import Polygon-specific values from a dictionary."""
	vertices_numpyified = []
	vertices = _validate_list(
		json_value.get("vertices"),
		error_prefix=f"{error_prefix}.vertices",
	)

	if len(vertices) < Polygon.MIN_VERTICES:
		raise ValueError(f"{error_prefix}.vertices must have at least 3 vertices")

	if len(vertices) == Triangle.REQUIRED_VERTICES:
		print(
			f"WARNING: {error_prefix} only has 3 vertices, automatically converting to Triangle"
		)
		return _load_triangle(json_value, error_prefix)

	for count, element in enumerate(vertices):
		vertex = _validate_position_vector(
			element,
			error_prefix=f"{error_prefix}.vertices[{count}]",
		)
		vertices_numpyified.append(vertex)

	return Polygon(vertices_numpyified)


def _load_triangle(json_value: dict, error_prefix: str = "Triangle") -> Triangle:
	"""Import Triangle-specific values from a dictionary."""
	vertices_numpyified = []
	vertices = _validate_list(
		json_value.get("vertices"),
		error_prefix=f"{error_prefix}.vertices",
	)

	if len(vertices) != Triangle.REQUIRED_VERTICES:
		raise ValueError(f"{error_prefix}.vertices must have 3 vertices")

	for count, element in enumerate(vertices):
		vertex = _validate_position_vector(
			element,
			error_prefix=f"{error_prefix}.vertices[{count}]",
		)
		vertices_numpyified.append(vertex)

	return Triangle(vertices_numpyified)


def _load_sphere(json_value: dict, error_prefix: str = "Sphere") -> Sphere:
	"""Import Sphere-specific values from a dictionary."""
	position = _validate_position_vector(
		json_value.get("position"),
		error_prefix=f"{error_prefix}.position",
	)
	radius = _validate_number(
		json_value.get("radius"),
		_min=0,
		error_prefix=f"{error_prefix}.radius",
	)

	return Sphere(position, radius)


def _validate_position_vector(
	json_value: Any | None,
	default: list[float] | None = None,
	error_prefix: str = "Position",
) -> NDArray[np.float64]:
	"""Import a list as a position vector."""
	json_value = _validate_list(
		json_value,
		length=3,
		default=default,
		error_prefix=error_prefix,
	)
	for element in json_value:
		_validate_number(
			element,
			error_prefix=f"{error_prefix} element",
		)

	return np.array(json_value)


def _validate_direction_vector(
	json_value: Any | None,
	default: list[float] | None = None,
	error_prefix: str = "Direction",
) -> NDArray[np.float64]:
	"""Import a list as a direction vector, verifying it is normalized."""
	json_value = _validate_list(
		json_value,
		length=3,
		default=default,
		error_prefix=error_prefix,
	)
	for element in json_value:
		_validate_number(
			element,
			error_prefix=f"{error_prefix} element",
		)

	# Convert to numpy array
	vector = np.array(json_value)

	# Make sure the vector is normalized
	mag = magnitude(vector)
	if mag not in (0, 1):
		print(
			f"WARNING: {error_prefix} is not normalized, performing auto-normalization"
		)
		vector = normalized(vector)
		print(
			f"WARNING: {error_prefix} has been normalized to [{vector[0]}, {vector[1]}, {vector[2]}]"
		)

	return vector


def _validate_color_vector(
	json_value: Any | None,
	default: list[float] | None = None,
	error_prefix: str = "Color",
) -> NDArray[np.float64]:
	"""Import a list as a color vector, verifying the proper range of values."""
	json_value = _validate_list(
		json_value,
		length=3,
		default=default,
		error_prefix=error_prefix,
	)
	for element in json_value:
		_validate_number(
			element,
			_min=0,
			_max=1,
			error_prefix=f"{error_prefix} element",
		)

	return np.array(json_value)


def _validate_list(
	json_value: Any | None,
	length: int | None = None,
	default: list | None = None,
	error_prefix: str = "List",
) -> list:
	"""Import a list and validates it against certain constraints."""
	if json_value is None and default is not None:
		print(
			f"WARNING: {error_prefix} is missing, reverting to default value {default}"
		)
		return default

	if json_value is None:
		raise ValueError(f"{error_prefix} must not be missing")
	if not isinstance(json_value, list):
		raise TypeError(f"{error_prefix} must be type list, not {type(json_value)}")
	if length is not None and len(json_value) != length:
		raise ValueError(
			f"{error_prefix} must have {length} elements, not {len(json_value)}"
		)

	return json_value


def _validate_number(
	json_value: Any | None,
	_min: float | None = None,
	_max: float | None = None,
	default: float | None = None,
	error_prefix: str = "Number",
) -> float | int:
	"""Import a number and validates it against certain constraints."""
	if json_value is None and default is not None:
		print(
			f"WARNING: {error_prefix} is missing, reverting to default value {default}"
		)
		return default

	if json_value is None:
		raise ValueError(f"{error_prefix} must not be missing")
	if not isinstance(json_value, float | int):
		raise TypeError(
			f"{error_prefix} must be type float or int, not {type(json_value)}"
		)
	if _min is not None and json_value < _min:
		raise ValueError(
			f"{error_prefix} must be greater than {_min}, not {json_value}"
		)
	if _max is not None and json_value > _max:
		raise ValueError(f"{error_prefix} must be less than {_max}, not {json_value}")

	return json_value
