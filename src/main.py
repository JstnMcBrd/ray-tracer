"""
The main script of the project.

Call it from the command line using `python ./src/main.py [arguments]`.
To see a full list of arguments, use `python ./src/main.py --help`.
"""


import argparse
from datetime import datetime
from os import getenv

from dotenv import load_dotenv

from ray_tracer import ray_trace
from scene_importer import import_scene
from writers import write_to_ppm


if __name__ == "__main__":

	# Default arguments
	DEFAULT_OUTPUT = "./output.ppm"
	DEFAULT_WIDTH = 512
	DEFAULT_HEIGHT = 512
	DEFAULT_MAX_COLOR = 255
	DEFAULT_REFLECTION_LIMIT = 10
	DEFAULT_PROGRESS_BAR = int(True)	# Must be an int because bools cannot be parsed from strings

	# Retrieve arguments from environment variables
	#	(All environment variables are imported as strings.
	# 	The ArgumentParser will take care of parsing them.)
	load_dotenv()
	env_scene = getenv("scene")
	env_output = getenv("output", default=DEFAULT_OUTPUT)
	env_width = getenv("width", default=str(DEFAULT_WIDTH))
	env_height = getenv("height", default=str(DEFAULT_HEIGHT))
	env_max_color = getenv("max-color", default=str(DEFAULT_MAX_COLOR))
	env_reflection_limit = getenv("reflection-limit", default=str(DEFAULT_REFLECTION_LIMIT))
	env_progress_bar = getenv("progress-bar", default=str(DEFAULT_PROGRESS_BAR))

	# Retrieve arguments overrides from command line
	#	(A command line argument is only required if the environment variable is missing.)
	arg = argparse.ArgumentParser("Ray Tracer")
	arg.add_argument("-s", "--scene", "-i", "--input", type=str, help="Path to the scene file",
		default=env_scene, required=env_scene is None)
	arg.add_argument("-o", "--output", type=str, help="Path to the output file",
		default=env_output, required=env_output is None)
	arg.add_argument("-x", "--width", type=int, help="Width of the output image",
		default=env_width, required=env_width is None)
	arg.add_argument("-y", "--height", type=int, help="Height of the output image",
		default=env_height, required=env_height is None)
	arg.add_argument("-c", "--max-color", type=float, help="Max color of the ppm file",
		default=env_max_color, required=env_max_color is None)
	arg.add_argument("-r", "--reflection-limit", type=int, help="Max number of recursive reflections",
		default=env_reflection_limit, required=env_reflection_limit is None)
	arg.add_argument("-p", "--progress-bar", type=bool, help="Whether to show a progress bar",
		default=env_progress_bar, required=env_progress_bar is None)

	# Parse arguments
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

	# Raytrace
	start_time = datetime.now()
	screen = ray_trace(scene, width, height, reflection_limit, progress_bar)
	end_time = datetime.now()

	# Print timer
	elapsed = end_time - start_time
	pixels_per_second = (width*height) / elapsed.total_seconds()
	print(f"Time elapsed:\t{elapsed}\t({int(pixels_per_second)} pixels/second)")

	# Write to file
	print("Writing to file... ", end="", flush=True)
	write_to_ppm(screen, output_file_path, max_color)
	print("Done", flush=True)
