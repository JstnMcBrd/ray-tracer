#!/usr/bin/python


"""
The main script of the system.

Call it from the command line using `python src [arguments]`.
To see a full list of arguments, use `python src --help`.
"""


from argparse import ArgumentParser
from datetime import UTC, datetime
from os import getenv

from dotenv import load_dotenv

from exporter import assert_supported_extension, export
from importer import import_scene
from ray_tracer import ray_trace

# Default arguments
DEFAULT_OUTPUT = "./output.png"
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_REFLECTION_LIMIT = 10
DEFAULT_PROGRESS_BAR = int(True) # Must be an int (bools cannot be parsed from strings)


def parse_arguments() -> tuple[str, str, int, int, int, bool]:
	"""Parse and return the environment variables and command-line arguments."""
	# Retrieve arguments from environment variables
	# (All environment variables are imported as strings.
	# The ArgumentParser will take care of parsing them.)
	load_dotenv()
	env_scene = getenv("scene")
	env_output = getenv("output", default=DEFAULT_OUTPUT)
	env_width = getenv("width", default=str(DEFAULT_WIDTH))
	env_height = getenv("height", default=str(DEFAULT_HEIGHT))
	env_reflection_limit = getenv("reflection-limit", default=str(DEFAULT_REFLECTION_LIMIT))
	env_progress_bar = getenv("progress-bar", default=str(DEFAULT_PROGRESS_BAR))

	# Retrieve arguments overrides from command line
	# (A command line argument is only required if the environment variable is missing.)
	arg = ArgumentParser("Ray Tracer")
	arg.add_argument("-s", "--scene", type=str,
		help="Path to the scene file",
		default=env_scene, required=env_scene is None)
	arg.add_argument("-o", "--output", type=str,
		help="Path to the output file",
		default=env_output, required=env_output is None)
	arg.add_argument("-x", "--width", type=int,
		help="Width of the output image",
		default=env_width, required=env_width is None)
	arg.add_argument("-y", "--height", type=int,
		help="Height of the output image",
		default=env_height, required=env_height is None)
	arg.add_argument("-r", "--reflection-limit", type=int,
		help="Max number of recursive reflections",
		default=env_reflection_limit, required=env_reflection_limit is None)
	arg.add_argument("-p", "--progress-bar", type=bool,
		help="Whether to show a progress bar",
		default=int(env_progress_bar), required=env_progress_bar is None)

	# Parse arguments
	parsed = arg.parse_args()
	scene_file_path: str = parsed.scene
	output_file_path: str = parsed.output
	width: int = parsed.width
	height: int = parsed.height
	reflection_limit: int = parsed.reflection_limit
	progress_bar: bool = parsed.progress_bar

	return scene_file_path, output_file_path, width, height, reflection_limit, progress_bar


def main(scene_file_path: str, output_file_path: str, width: int, height: int, reflection_limit: int, progress_bar: bool) -> None:
	"""Import, ray-trace, and export."""
	# Assert the output file extension is supported
	assert_supported_extension(output_file_path)

	# Import Scene
	print()
	print("> Importing...")
	start_time = datetime.now(UTC)
	scene = import_scene(scene_file_path)
	time_elapsed = datetime.now(UTC) - start_time
	print(f"Time elapsed: {time_elapsed}")
	print("> Done")
	print()

	# Raytrace
	print("> Ray tracing...")
	start_time = datetime.now(UTC)
	screen = ray_trace(scene, width, height, reflection_limit, progress_bar)
	time_elapsed = datetime.now(UTC) - start_time
	print(f"Time elapsed: {time_elapsed}")
	print("> Done")
	print()

	# Export to file
	print("> Exporting...")
	start_time = datetime.now(UTC)
	export(screen, output_file_path)
	time_elapsed = datetime.now(UTC) - start_time
	print(f"Time elapsed: {time_elapsed}")
	print("> Done")
	print()


if __name__ == "__main__":
	main(*parse_arguments())
