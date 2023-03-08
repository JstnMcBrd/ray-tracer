import numpy as np

import objects.Object as Object
from Scene import Scene

def shade(scene: Scene, obj: Object, location: np.ndarray, view_direction: np.ndarray, shadow: bool) -> np.ndarray:
	shadow_coefficient = 0 if shadow else 1

	surface_normal = obj.normal(location)

	N_dot_L = np.dot(surface_normal, scene.direction_to_light)
	reflected = 2 * surface_normal * N_dot_L - scene.direction_to_light

	ambient = obj.ambient_coefficient * scene.ambient_light_color * obj.diffuse_color
	diffuse = shadow_coefficient * obj.diffuse_coefficient * scene.light_color * obj.diffuse_color * max(0, N_dot_L)
	specular = shadow_coefficient * obj.specular_coefficient * scene.light_color * obj.specular_color * max(0, np.dot(view_direction, reflected))**obj.gloss_coefficient
	color = ambient + diffuse + specular
	
	color = np.clip(color, 0, 1)

	return color
