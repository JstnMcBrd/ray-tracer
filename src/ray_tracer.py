from math import tan
import numpy as np

from Scene import Object, Scene

def ray_trace(scene: Scene, width: int, height: int) -> np.ndarray:
	screen = np.zeros((width, height, 3)) # TODO this is time/space intensive - maybe calculate + write values gradually?

	# Get camera axes and positions
	camera_look_from = scene.camera_look_from
	camera_look_at = scene.camera_look_at
	camera_forward = scene.camera_forward()
	camera_up = scene.camera_up()
	camera_right = scene.camera_right()

	# Calculate screen sizes
	viewport_size = np.array([width, height])
	window_size = calculate_window_size(viewport_size, camera_look_at, camera_look_from, scene.field_of_view)

	# Save time by pre-calcuating constant values
	window_to_viewport_size_ratio = window_size/viewport_size
	half_window_size = window_size/2
	ray_origin = camera_look_from

	# For each pixel on the screen...
	for x in range(len(screen)):
		for y in range(len(screen[x])):
			# Find the world point of the pixel
			viewport_point = np.array([x, y])
			window_point = viewport_to_window(viewport_point, window_to_viewport_size_ratio, half_window_size)
			world_point = window_to_world(window_point, camera_forward, camera_look_at, camera_up, camera_right)

			# Find the direction the ray is pointing
			ray_direction = normalize(world_point - camera_look_from)

			# Find the closest object that intersects with the ray
			closest_object: Object = None
			closest_intersection = None
			closest_distance = float("inf")
			closest_direction = None
			for obj in scene.objects:
				intersection = obj.ray_intersection(ray_origin, ray_direction)
				if not type(intersection) is type(None):
					direction = camera_look_from - intersection
					distance = magnitude(direction)
					if distance < closest_distance:
						closest_object = obj
						closest_intersection = intersection
						closest_distance = distance
						closest_direction = direction

			# Shade the pixel using the closest object
			if closest_object != None:
				view_direction = closest_direction / closest_distance # Normalize
				normal = closest_object.normal(closest_intersection)
				screen[x,y] = shading(scene, closest_object, normal, view_direction)
			
			# If no object collided, use the background
			else:
				screen[x,y] = scene.background_color

	return screen


def magnitude(vector: np.ndarray) -> float:
	return np.sqrt(np.dot(vector, vector))


def normalize(vector: np.ndarray) -> np.ndarray:
	return vector / magnitude(vector)


def calculate_window_size(viewport_size: np.ndarray, camera_look_from: np.ndarray, camera_look_at: np.ndarray, field_of_view: float) -> np.ndarray:
	dist = camera_look_at - camera_look_from
	dist_mag = magnitude(dist)
	x = dist_mag * tan(np.deg2rad(field_of_view/2)) * 2
	y = x * viewport_size[1]/viewport_size[0]
	return np.array([x, y])


def viewport_to_window(viewport_point: np.ndarray, window_to_viewport_size_ratio: np.ndarray, half_window_size: np.ndarray) -> np.ndarray:
	window_point = viewport_point * window_to_viewport_size_ratio - half_window_size
	return np.array([window_point[0], window_point[1]*-1, 0]) # The -1 seems necessary to orient it correctly


def window_to_world(window_point: np.ndarray, camera_look_at: np.ndarray, camera_forward: np.ndarray, camera_up: np.ndarray, camera_right: np.ndarray) -> np.ndarray:
	return camera_look_at + window_point[0]*camera_right + window_point[1]*camera_up + window_point[2]*camera_forward


def shading(scene: Scene, obj: Object, surface_normal: np.ndarray, view_direction: np.ndarray) -> np.ndarray:
	N_dot_L = np.dot(surface_normal, scene.direction_to_light)
	reflected = 2 * surface_normal * N_dot_L - scene.direction_to_light

	ambient = obj.ambient_coefficient * scene.ambient_light_color * obj.diffuse_color
	diffuse = obj.diffuse_coefficient * scene.light_color * obj.diffuse_color * max(0, N_dot_L)
	specular = obj.specular_coefficient * scene.light_color * obj.specular_color * max(0, np.dot(view_direction, reflected))**obj.gloss_coefficient
	return ambient + diffuse + specular
