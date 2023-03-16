"""
Contains methods for writing the screen to image files.
"""
# TODO add support for other image types


import numpy as np


def write_to_ppm(screen: np.ndarray, output_file_path: str, max_color: float):
	""" Writes the screen to a file with [PPM](https://en.wikipedia.org/wiki/Netpbm) encoding. """

	with open(output_file_path, mode="w", encoding="utf8") as output_file:
		# Headers
		output_file.write("P3\n")
		output_file.write(f"{len(screen)} {len(screen[0])}\n")
		output_file.write(f"{max_color}\n")

		# Pixels
		for y in range(len(screen[0])):
			for x in range(len(screen)):
				pixel = screen[x,y]*max_color
				output_file.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
			output_file.write("\n")
