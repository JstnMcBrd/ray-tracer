"""
Contains methods for writing the screen to image files.
"""


import numpy as np

from tqdm import tqdm


def write_to_ppm(screen: np.ndarray, output_file_path: str, max_color: float, progress_bar: bool):
	""" Writes the screen to a file with [PPM](https://en.wikipedia.org/wiki/Netpbm) encoding. """

	with open(output_file_path, mode="w", encoding="utf8") as output_file:
		# Headers
		output_file.write("P3\n")
		output_file.write(f"{len(screen)} {len(screen[0])}\n")
		output_file.write(f"{max_color}\n")

		# Pixels
		pixels = [(x,y) for y in range(len(screen[0])) for x in range(len(screen))]
		if progress_bar:
			pixels = tqdm(pixels)
		for x,y in pixels:
			pixel = screen[x,y]*max_color
			output_file.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
