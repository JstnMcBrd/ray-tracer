import argparse
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

from ray_tracer import ray_trace
from scene_importer import import_scene
from Scene import Scene
from writers import write_to_ppm


# TODO shadows
# TODO reflection
# TODO refraction
# TODO more than one light source


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

	# Import Scene
	scene = import_scene(scene_file_path)

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
