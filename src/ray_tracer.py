"""
Generates an image from a scene using
[ray tracing](https://en.wikipedia.org/wiki/Ray_tracing_(graphics)).
"""


from math import tan
from multiprocessing import Pool, cpu_count
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
from ray import Ray
from scene import Camera, Scene
from shader import shade
from tqdm import tqdm
from vector import normalized


FADE_LIMIT = 0.01
"Fading limit for reflections"

COLLISION_NORMAL_OFFSET = 0.01
"Offsets collision positions from the surfaces of objects to avoid incorrect shadows"


def ray_trace(scene: Scene, width: int, height: int,
		reflection_limit: int, progress_bar: bool) -> NDArray[np.float_]:
	"""
	Ray traces the given scene and returns a 3-dimensional array of pixel colors
	with `shape=(height, width, 3)`.
	"""

	# Save time by pre-calcuating constant values
	viewport_size = np.array([width, height])
	window_size = _get_window_size(viewport_size,
					scene.camera.focal_length, scene.camera.field_of_view)
	window_to_viewport_size_ratio = window_size/viewport_size
	half_window_size = window_size/2

	# Set up multiprocessing pool and inputs
	tuple_inputs = [(scene, reflection_limit, x, y, window_to_viewport_size_ratio, half_window_size)
		for y in range(height) for x in range(width)]
	outputs = []

	with Pool(cpu_count()) as pool:

		# Start a process for ray-tracing each pixel
		processes: Iterable = pool.imap(_ray_trace_pixel_tuple, tuple_inputs)
		if progress_bar:
			processes = tqdm(processes, total=len(tuple_inputs))

		# Iterate and store the output to allow it to compute
		outputs = list(processes)

	# Shape outputs into a width*height screen
	screen = np.array(outputs)
	_, depth = screen.shape
	screen.resize((height, width, depth))

	return screen


def _ray_trace_pixel_tuple(
		tuple_input: tuple[Scene, int, int, int, NDArray[np.float_], NDArray[np.float_]]
	) -> NDArray[np.float_]:
	"Unpacks the tuple input for _ray_trace_pixel and returns the result."

	return _ray_trace_pixel(*tuple_input)


def _ray_trace_pixel(
		scene: Scene, reflection_limit: int, x: int, y: int,
		window_to_viewport_size_ratio: NDArray[np.float_], half_window_size: NDArray[np.float_]
	) -> NDArray[np.float_]:
	"Retrieves the color for a given pixel."

	# Find the world point of the pixel, relative to the camera's position
	viewport_point = np.array([x, y])
	window_point = _viewport_to_window(viewport_point, window_to_viewport_size_ratio, half_window_size)
	world_point_relative = _window_to_relative_world(window_point, scene.camera)

	# Start sending out rays
	return _get_color(scene, reflection_limit,
			scene.camera.position, normalized(world_point_relative))


def _get_color(scene: Scene, reflection_limit: int,
		origin: NDArray[np.float_], direction: NDArray[np.float_],
		fade=1, reflections=0) -> NDArray[np.float_]:
	"Recursively casts rays to retrieve the color for the original ray collision."

	if fade <= FADE_LIMIT or reflections > reflection_limit:
		return np.array([0,0,0])

	# Initialize and cast the ray
	ray = Ray(origin, direction)
	collision = scene.cast_ray(ray)

	# Shade the pixel using the collided object
	if collision is not None:

		# Shadows
			# Avoid getting trapped inside objects
		normal = collision.obj.normal(collision.position)
		collision.position += COLLISION_NORMAL_OFFSET*normal
		shadow = _is_in_shadow(scene, collision.position)

		# Reflections (recursive)
		sight_reflection_direction = ray.direction - 2 * normal * np.dot(ray.direction, normal)
		reflected_color = _get_color(scene, reflection_limit, collision.position,
						sight_reflection_direction, fade*collision.obj.reflectivity, reflections+1)

		# Shading
		view_direction = -1 * ray.direction
		return shade(scene, collision.obj, collision.position, view_direction, shadow, reflected_color)

	# If no object collided, use the background
	return scene.background_color


def _is_in_shadow(scene: Scene, point: NDArray[np.float_]) -> bool:
	"Casts a ray toward the light source to determine if the point is in shadow."

	ray = Ray(point, scene.light_direction)
	collision = scene.cast_ray(ray)
	return collision is not None


def _get_window_size(viewport_size: NDArray[np.int_], focal_length: float, field_of_view: float
	) -> NDArray[np.float_]:
	"Returns the window size, given the camera properties."

	x = focal_length * tan(np.deg2rad(field_of_view/2)) * 2
	y = x * viewport_size[1]/viewport_size[0]
	return np.array([x, y])


def _viewport_to_window(viewport_point: NDArray[np.float_],
			window_to_viewport_size_ratio: NDArray[np.float_],
			half_window_size: NDArray[np.float_]) -> NDArray[np.float_]:
	"Converts a point on the viewport to a point on the window."

	window_point = viewport_point * window_to_viewport_size_ratio - half_window_size
	# The -1 seems necessary to orient it correctly
	window_point[1] *= -1
	return np.concatenate([window_point, [0]])


def _window_to_relative_world(window_point: NDArray[np.float_], camera: Camera
	) -> NDArray[np.float_]:
	"Converts a point on the window to world point (relative to the camera)."

	axes = np.array([camera.right, camera.up, camera.forward])
	return camera.relative_look_at + np.dot(window_point, axes)
