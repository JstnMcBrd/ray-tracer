"""
Generates an image from a scene using
[ray tracing](https://en.wikipedia.org/wiki/Ray_tracing_(graphics)).
"""


from math import tan
from multiprocessing import cpu_count, Pool
import numpy as np
from tqdm import tqdm

from lib._multiprocessing import istarmap
from ray import Ray
from scene import Camera, Scene
from shader import shade
from vector import normalized


def ray_trace(scene: Scene, width: int, height: int,
		reflection_limit: int, progress_bar: bool) -> np.ndarray:
	""" Ray traces the given scene and returns a numpy array of pixel colors. """

	camera = scene.camera

	# Save time by pre-calcuating constant values
	num_pixels = width*height
	viewport_size = np.array([width, height])
	window_size = _calculate_window_size(viewport_size, camera.focal_length, camera.field_of_view)
	window_to_viewport_size_ratio = window_size/viewport_size
	half_window_size = window_size/2

	# Set up multiprocessing pool and inputs
	inputs = [(x, y, scene, window_to_viewport_size_ratio, half_window_size, reflection_limit)
		for x in range(width) for y in range(height)]
	outputs = []

	with Pool(cpu_count()) as pool:

		# Start a process for ray-tracing each pixel
		processes = istarmap(pool, _ray_trace_pixel, inputs)
		if progress_bar:
			processes = tqdm(processes, total=num_pixels)

		# Iterate and store the output to allow it to compute
		outputs = [output for output in processes]

	# Shape outputs into a width*height screen
	screen = np.array(outputs).reshape((width, height, 3))

	return screen


def _ray_trace_pixel(x: int, y: int, scene: Scene,
			window_to_viewport_size_ratio: np.ndarray, half_window_size: np.ndarray,
			reflection_limit: int) -> np.ndarray:
	""" Retrieves the color for a given pixel. """

	# Find the world point of the pixel, relative to the camera's position
	viewport_point = np.array([x, y])
	window_point = _viewport_to_window(viewport_point, window_to_viewport_size_ratio, half_window_size)
	world_point_relative = _window_to_relative_world(window_point, scene.camera)

	# Start sending out rays
	return _get_color(scene.camera.position, normalized(world_point_relative), scene,
			reflection_limit=reflection_limit)


def _get_color(origin: np.ndarray, direction: np.ndarray, scene: Scene,
		fade=1, reflections=0, reflection_limit=float("inf")):
	""" Recursively casts rays to retrieve the color for the original ray collision. """

	if fade <= 0.01 or reflections > reflection_limit:
		return np.array([0,0,0])

	# Initialize and cast the ray
	ray = Ray(origin, direction)
	collision = ray.cast(scene)

	# Shade the pixel using the collided object
	if collision is not None:
		view_direction = -1 * ray.direction
		normal = collision.obj.normal(collision.position)

		# Avoid getting trapped inside objects
		collision.position += 0.01*normal

		shadow = _is_in_shadow(collision.position, scene)

		sight_reflection_direction = ray.direction - 2 * normal * np.dot(ray.direction, normal)
		# Avoid colliding with the same surface
		offset_origin = collision.position + 0.01*sight_reflection_direction

		# Get the color from the reflection (recursive)
		reflected_color = _get_color(offset_origin, sight_reflection_direction, scene,
						fade=fade*collision.obj.reflectivity, reflections=reflections+1,
						reflection_limit=reflection_limit)

		return shade(scene, collision.obj, collision.position, view_direction, shadow, reflected_color)

	# If no object collided, use the background
	return scene.background_color


def _is_in_shadow(point: np.ndarray, scene: Scene) -> bool:
	""" Casts a ray toward the light source to determine if the point is in shadow. """

	ray = Ray(point, scene.light_direction)
	ray.origin += ray.direction * 0.01	# Offset to avoid colliding with the object

	collision = ray.cast(scene)
	return collision is not None


def _calculate_window_size(viewport_size: np.ndarray,
				focal_length: np.ndarray,
				field_of_view: float) -> np.ndarray:
	""" Returns the window size, given the camera properties. """

	x = focal_length * tan(np.deg2rad(field_of_view/2)) * 2
	y = x * viewport_size[1]/viewport_size[0]
	return np.array([x, y])


def _viewport_to_window(viewport_point: np.ndarray,
			window_to_viewport_size_ratio: np.ndarray,
			half_window_size: np.ndarray) -> np.ndarray:
	""" Converts a point on the viewport to a point on the window. """

	window_point = viewport_point * window_to_viewport_size_ratio - half_window_size
	# The -1 seems necessary to orient it correctly
	return np.array([window_point[0], window_point[1]*-1, 0])


def _window_to_relative_world(window_point: np.ndarray, camera: Camera) -> np.ndarray:
	""" Converts a point on the window to world point (relative to the camera). """

	return camera.relative_look_at \
		+ window_point[0]*camera.right \
			+ window_point[1]*camera.up \
				+ window_point[2]*camera.forward
