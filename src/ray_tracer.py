from math import tan
import numpy as np

from objects.Object import Object
from Ray import Ray
from Scene import Scene
from shader import shade
from vector_utils import magnitude, normalized


# TODO refraction
# TODO more than one light source
# TODO multiprocessing


def ray_trace(scene: Scene, width: int, height: int, reflection_limit:int) -> np.ndarray:
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

			screen[x,y] = get_color(camera_look_from, normalized(world_point_relative), scene, reflection_limit=reflection_limit)

		# Report progress
		pixel_num += width
		percent_progress += one_row_progress
		percent_progress_one_decimal = int(percent_progress*10)/10

		print("\r", end="", flush=True) # Wipe the previous line of output
		print(f"Progress:\t{percent_progress_one_decimal}%\t\t({pixel_num}/{num_pixels} pixels)", end="", flush=True)

	print()
	return screen


def is_in_shadow(point: np.ndarray, scene: Scene) -> bool:
	ray = Ray(point, scene.direction_to_light)
	ray.origin += ray.direction * 0.01	# Offset to avoid colliding with the object
	
	collision = ray.cast(scene)
	return collision is not None


def get_color(origin: np.ndarray, direction: np.ndarray, scene: Scene, fade=1, reflections=0, reflection_limit=float("inf")):
	if fade <= 0.01 or reflections > reflection_limit:
		return np.array([0,0,0])

	# Initialize and cast the ray
	ray = Ray(origin, direction)
	collision = ray.cast(scene)

	# Shade the pixel using the collided object
	if collision is not None:
		view_direction = -1 * ray.direction
		normal = collision.obj.normal(collision.location)

		collision.location += 0.01*normal	# Avoid getting trapped inside objects

		shadow = is_in_shadow(collision.location, scene)

		reflection_direction = ray.direction - 2 * normal * np.dot(ray.direction, normal)
		offset_origin = collision.location + 0.01*reflection_direction	# Avoid colliding with the same surface

		reflected_color = get_color(offset_origin, reflection_direction, scene, fade=fade*collision.obj.reflectivity, reflections=reflections+1, reflection_limit=reflection_limit)

		return shade(scene, collision.obj, collision.location, view_direction, shadow, reflected_color)		

	# If no object collided, use the background
	else:
		return scene.background_color


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
