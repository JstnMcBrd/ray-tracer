import numpy as np

import objects.Object as Object
from Scene import Scene

# Phong shading
def shade(scene: Scene, obj: Object, location: np.ndarray, view_direction: np.ndarray, shadow: bool, reflected_color: np.ndarray) -> np.ndarray:
	shadow_coefficient = 0 if shadow else 1

	surface_normal = obj.normal(location)

	N_dot_L = np.dot(surface_normal, scene.light_direction)
	reflection_direction = 2 * surface_normal * N_dot_L - scene.light_direction

	ambient = obj.ambient_coefficient * scene.ambient_light_color * obj.diffuse_color
	diffuse = shadow_coefficient * obj.diffuse_coefficient * scene.light_color * obj.diffuse_color * max(0, N_dot_L)
	specular = shadow_coefficient * obj.specular_coefficient * scene.light_color * obj.specular_color * max(0, np.dot(view_direction, reflection_direction))**obj.gloss_coefficient
	reflected = obj.reflectivity * reflected_color
	color = ambient + diffuse + specular + reflected
	
	color = np.clip(color, 0, 1)

	return color
