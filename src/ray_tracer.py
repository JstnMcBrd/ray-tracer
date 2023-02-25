from math import tan
import numpy as np

from Scene import Object, Scene
from shader import shade

def ray_trace(scene: Scene, width: int, height: int) -> np.ndarray:
	screen = np.zeros((width, height, 3)) # TODO this is time/space intensive - maybe calculate + write values gradually?
	num_pixels = width * height

	# Get camera axes and positions
	camera_look_from = scene.camera_look_from
	camera_look_at = scene.camera_look_at
	camera_forward = scene.camera_forward()
	camera_up = scene.camera_up()
	camera_right = scene.camera_right()

	# Save time by pre-calcuating constant values
	camera_look_at_relative = camera_look_at - camera_look_from

	viewport_size = np.array([width, height])
	window_size = calculate_window_size(viewport_size, camera_look_at_relative, scene.field_of_view)
	window_to_viewport_size_ratio = window_size/viewport_size
	half_window_size = window_size/2

	ray_origin = camera_look_from

	# For each pixel on the screen...
	pixel_num = 0
	percent_progress = 0
	one_row_progress = (width/num_pixels)*100
	for x in range(len(screen)):
		for y in range(len(screen[x])):
			# Find the world point of the pixel, relative to the camera's position
			viewport_point = np.array([x, y])
			window_point = viewport_to_window(viewport_point, window_to_viewport_size_ratio, half_window_size)
			world_point_relative = window_to_relative_world(window_point, camera_look_at_relative, camera_forward, camera_up, camera_right)

			# Find the direction the ray is pointing
			ray_direction = normalize(world_point_relative)

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
				screen[x,y] = shade(scene, closest_object, normal, view_direction)
			
			# If no object collided, use the background
			else:
				screen[x,y] = scene.background_color

		# Report progress
		pixel_num += width
		percent_progress += one_row_progress
		percent_progress_one_decimal = int(percent_progress*10)/10

		print("\r", end="", flush=True) # Wipe the previous line of output
		print(f"Progress:\t{percent_progress_one_decimal}%\t\t({pixel_num}/{num_pixels} pixels)", end="", flush=True)

	print()
	return screen


def magnitude(vector: np.ndarray) -> float:
	return np.sqrt(np.dot(vector, vector))


def normalize(vector: np.ndarray) -> np.ndarray:
	return vector / magnitude(vector)


def calculate_window_size(viewport_size: np.ndarray, camera_look_at_relative: np.ndarray, field_of_view: float) -> np.ndarray:
	distance = magnitude(camera_look_at_relative)
	x = distance * tan(np.deg2rad(field_of_view/2)) * 2
	y = x * viewport_size[1]/viewport_size[0]
	return np.array([x, y])


def viewport_to_window(viewport_point: np.ndarray, window_to_viewport_size_ratio: np.ndarray, half_window_size: np.ndarray) -> np.ndarray:
	window_point = viewport_point * window_to_viewport_size_ratio - half_window_size
	return np.array([window_point[0], window_point[1]*-1, 0]) # The -1 seems necessary to orient it correctly


def window_to_relative_world(window_point: np.ndarray, camera_look_at_relative: np.ndarray, camera_forward: np.ndarray, camera_up: np.ndarray, camera_right: np.ndarray) -> np.ndarray:
	return camera_look_at_relative + window_point[0]*camera_right + window_point[1]*camera_up + window_point[2]*camera_forward
