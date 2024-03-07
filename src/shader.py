"Contains methods for shading objects."


import numpy as np
from numpy.typing import NDArray

from objects import Object
from scene import Scene


def shade(scene: Scene, obj: Object, position: NDArray[np.float_],
		view_direction: NDArray[np.float_], shadow: bool, reflected_color: NDArray[np.float_]
	) -> NDArray[np.float_]:
	"""
	Applies [Phong shading](https://en.wikipedia.org/wiki/Phong_shading)
	to the given object and returns the color.
	"""

	shadow_coefficient = 0 if shadow else 1

	surface_normal = obj.normal(position)
	normal_dot_light = np.dot(surface_normal, scene.light_direction)
	light_reflection_direction = 2 * surface_normal * normal_dot_light - scene.light_direction
	view_dot_light = np.dot(view_direction, light_reflection_direction)

	# Ambient lighting
	ambient = scene.ambient_light_color * obj.diffuse_color
	ambient *= obj.ambient_coefficient

	# Diffuse lighting
	diffuse = scene.light_color * obj.diffuse_color * max(0, normal_dot_light)
	diffuse *= obj.diffuse_coefficient
	diffuse *= shadow_coefficient

	# Specular lighting
	specular = scene.light_color * obj.specular_color * max(0, view_dot_light)**obj.gloss_coefficient
	specular *= obj.specular_coefficient
	specular *= shadow_coefficient

	# Reflections
	reflected = obj.reflectivity * reflected_color

	# Combined color
	color = ambient + diffuse + specular + reflected
	color = np.clip(color, 0, 1)

	return color
