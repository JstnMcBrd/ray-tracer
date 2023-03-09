from math import tan
import lib_patches.istarmap
from multiprocessing import cpu_count, Pool
import numpy as np
import tqdm

from objects.Object import Object
from Ray import Ray
from Scene import Camera, Scene
from shader import shade
from vector_utils import magnitude, normalized


# TODO refraction
# TODO more than one light source


def ray_trace(scene: Scene, width: int, height: int, reflection_limit:int, progress_bar: bool) -> np.ndarray:
	# Save time by pre-calcuating constant values
	num_pixels = width*height
	viewport_size = np.array([width, height])
	window_size = calculate_window_size(viewport_size, scene.camera.focal_length, scene.camera.field_of_view)
	window_to_viewport_size_ratio = window_size/viewport_size
	half_window_size = window_size/2

	# Set up multiprocessing pool and inputs
	pool = Pool(cpu_count())
	inputs = [(x, y, scene, window_to_viewport_size_ratio, half_window_size, reflection_limit) for x in range(width) for y in range(height)]

	# Start a process for ray-tracing each pixel
	processes = pool.istarmap(ray_trace_pixel, inputs)
	if progress_bar:
		processes = tqdm.tqdm(processes, total=num_pixels)

	# Iterate and store the output to allow it to compute
	outputs = [output for output in processes]

	# Shape outputs into a width*height screen
	screen = np.array(outputs).reshape((width, height, 3))

	return screen


def ray_trace_pixel(x: int, y: int, scene: Scene, window_to_viewport_size_ratio: np.ndarray, half_window_size: np.ndarray, reflection_limit: int) -> np.ndarray:	
	# Find the world point of the pixel, relative to the camera's position
	viewport_point = np.array([x, y])
	window_point = viewport_to_window(viewport_point, window_to_viewport_size_ratio, half_window_size)
	world_point_relative = window_to_relative_world(window_point, scene.camera)

	# Start sending out rays
	return get_color(scene.camera.position, normalized(world_point_relative), scene, reflection_limit=reflection_limit)


# Recursive
def get_color(origin: np.ndarray, direction: np.ndarray, scene: Scene, fade=1, reflections=0, reflection_limit=float("inf")):
	if fade <= 0.01 or reflections > reflection_limit:
		return np.array([0,0,0])

	# Initialize and cast the ray
	ray = Ray(origin, direction)
	collision = ray.cast(scene)

	# Shade the pixel using the collided object
	if collision is not None:
		view_direction = -1 * ray.direction
		normal = collision.obj.normal(collision.position)

		collision.position += 0.01*normal	# Avoid getting trapped inside objects

		shadow = is_in_shadow(collision.position, scene)

		reflection_direction = ray.direction - 2 * normal * np.dot(ray.direction, normal)
		offset_origin = collision.position + 0.01*reflection_direction	# Avoid colliding with the same surface

		reflected_color = get_color(offset_origin, reflection_direction, scene, fade=fade*collision.obj.reflectivity, reflections=reflections+1, reflection_limit=reflection_limit)

		return shade(scene, collision.obj, collision.position, view_direction, shadow, reflected_color)		

	# If no object collided, use the background
	else:
		return scene.background_color


def is_in_shadow(point: np.ndarray, scene: Scene) -> bool:
	ray = Ray(point, scene.light_direction)
	ray.origin += ray.direction * 0.01	# Offset to avoid colliding with the object
	
	collision = ray.cast(scene)
	return collision is not None


def calculate_window_size(viewport_size: np.ndarray, focal_length: np.ndarray, field_of_view: float) -> np.ndarray:
	x = focal_length * tan(np.deg2rad(field_of_view/2)) * 2
	y = x * viewport_size[1]/viewport_size[0]
	return np.array([x, y])


def viewport_to_window(viewport_point: np.ndarray, window_to_viewport_size_ratio: np.ndarray, half_window_size: np.ndarray) -> np.ndarray:
	window_point = viewport_point * window_to_viewport_size_ratio - half_window_size
	return np.array([window_point[0], window_point[1]*-1, 0]) # The -1 seems necessary to orient it correctly


def window_to_relative_world(window_point: np.ndarray, camera: Camera) -> np.ndarray:
	return camera.relative_look_at + window_point[0]*camera.right + window_point[1]*camera.up + window_point[2]*camera.forward
