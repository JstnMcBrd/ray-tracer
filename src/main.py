import argparse
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

from ray_tracer import ray_trace
from scene_importer import import_scene
from Scene import Scene
from writers import write_to_ppm


if __name__ == "__main__":
	# Retrieve arguments
	load_dotenv()

	arg = argparse.ArgumentParser("Ray Tracer")
	arg.add_argument("-s", "--scene", type=str, help="Path to the scene file", default=getenv("scene"), required=getenv("scene") is None)
	arg.add_argument("-o", "--output", type=str, help="Path to the output file", default=getenv("output"), required=getenv("output") is None)
	arg.add_argument("-x", "--width", type=int, help="Width of the output image", default=getenv("width"), required=getenv("width") is None)
	arg.add_argument("-y", "--height", type=int, help="Height of the output image", default=getenv("height"), required=getenv("height") is None)
	arg.add_argument("-c", "--max-color", type=float, help="The maximum color of the ppm file", default=getenv("max-color", default=255), required=getenv("max-color", default=255) is None)
	arg.add_argument("-r", "--reflection-limit", type=float, help="The maximum number of recursive reflections", default=getenv("reflection-limit", default=10), required=getenv("reflection-limit", default=10) is None)
	arg.add_argument("-p", "--progress-bar", type=bool, help="Whether to show a progress bar", default=bool(int(getenv("progress-bar", default=True))), required=bool(int(getenv("progress-bar", default=True))) is None)
	parsed = arg.parse_args()
	
	scene_file_path = parsed.scene
	output_file_path = parsed.output
	width = parsed.width
	height = parsed.height
	max_color = parsed.max_color
	reflection_limit = parsed.reflection_limit
	progress_bar = parsed.progress_bar

	# Import Scene
	scene = import_scene(scene_file_path)

	# Start timer
	start_time = datetime.now()

	# Raytrace
	screen = ray_trace(scene, width, height, reflection_limit, progress_bar)

	# Print timer
	end_time = datetime.now()
	elapsed = end_time - start_time
	pixels_per_second = (width*height) / elapsed.total_seconds()
	print(f"Time elapsed:\t{elapsed}\t({int(pixels_per_second)} pixels/second)")

	# Write to file
	print("Writing to file... ", end="", flush=True)
	write_to_ppm(screen, output_file_path, max_color)
	print("Done", flush=True)
