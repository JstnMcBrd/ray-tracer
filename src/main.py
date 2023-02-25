import argparse
from datetime import datetime
from dotenv import load_dotenv
import json
import numpy as np
from os import getenv

from ray_tracer import ray_trace
from scene_importer import load_from_json
from Scene import Scene


# TODO shadows
# TODO reflection
# TODO refraction
# TODO more than one light source


def load_scene(file_path: str) -> Scene:
	json_file = None
	try:
		json_file = open(file_path, "r")
	except Exception as err:
		print(f"\"{file_path}\" is not a valid path\n\t{err}")
		exit(1)

	json_data = None
	try:
		json_data = json.loads(json_file.read())
	except Exception as err:
		print(f"\"{file_path}\" is not a valid json file\n\t{err}")
		exit(1)

	scene = None
	try:
		scene = load_from_json(json_data)
	except AssertionError as err:
		print(f"\"{file_path}\" is improperly formatted\n\t{err}")
		exit(1)

	return scene


def write_to_ppm(screen: np.ndarray, output_file_path: str, max_color: float):
	output_file = open(output_file_path, "w")
	output_file.write("P3\n")
	output_file.write(f"{len(screen)} {len(screen[0])}\n")
	output_file.write(f"{max_color}\n")
	for y in range(len(screen[0])):
		for x in range(len(screen)):
			pixel = screen[x,y]*max_color
			output_file.write(f"{pixel[0]} {pixel[1]} {pixel[2]}     ")
		output_file.write("\n")


if __name__ == "__main__":
	load_dotenv()

	arg = argparse.ArgumentParser("Ray Tracer")
	arg.add_argument("-s", "--scene", type=str, help="Path to the scene file", default=getenv("SCENE"), required=getenv("SCENE") == None)
	arg.add_argument("-o", "--output", type=str, help="Path to the output file", default=getenv("OUTPUT"), required=getenv("OUTPUT") == None)
	arg.add_argument("-x", "--width", type=int, help="Width of the output image", default=getenv("WIDTH"), required=getenv("WIDTH") == None)
	arg.add_argument("-y", "--height", type=int, help="Height of the output image", default=getenv("HEIGHT"), required=getenv("HEIGHT") == None)
	arg.add_argument("-c", "--max-color", type=float, help="The maximum color of the ppm file", default=getenv("MAX_COLOR", default=255), required=getenv("MAX_COLOR", default=255) == None)
	parsed = arg.parse_args()
	
	# Arguments
	scene_file_path = parsed.scene
	output_file_path = parsed.output
	width = parsed.width
	height = parsed.height
	max_color = parsed.max_color

	# Start timer
	start_time = datetime.now()

	# Load Scene
	scene = load_scene(scene_file_path)

	# Raytrace
	screen = ray_trace(scene, width, height)

	# Write to file
	write_to_ppm(screen, output_file_path, max_color)

	# Print timer
	end_time = datetime.now()
	elapsed = end_time - start_time
	pixels_per_second = (width*height) / elapsed.total_seconds()

	print(f"Time elapsed:\t{elapsed}\t({int(pixels_per_second)} pixels/second)")
	print
