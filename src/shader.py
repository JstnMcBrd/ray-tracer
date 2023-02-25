import numpy as np

from Scene import Object, Scene

def shade(scene: Scene, obj: Object, surface_normal: np.ndarray, view_direction: np.ndarray) -> np.ndarray:
	N_dot_L = np.dot(surface_normal, scene.direction_to_light)
	reflected = 2 * surface_normal * N_dot_L - scene.direction_to_light

	ambient = obj.ambient_coefficient * scene.ambient_light_color * obj.diffuse_color
	diffuse = obj.diffuse_coefficient * scene.light_color * obj.diffuse_color * max(0, N_dot_L)
	specular = obj.specular_coefficient * scene.light_color * obj.specular_color * max(0, np.dot(view_direction, reflected))**obj.gloss_coefficient
	return ambient + diffuse + specular
