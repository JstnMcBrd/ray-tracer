"""
Contains methods for writing the screen to image files.
"""


import numpy as np

from PIL import Image
from tqdm import tqdm


def write_to_ppm(screen: np.ndarray, output_file_path: str, progress_bar: bool):
	""" Writes the screen to a file with [PPM](https://en.wikipedia.org/wiki/Netpbm) encoding. """

	max_color = 255
	with open(output_file_path, mode="w", encoding="utf8") as output_file:
		# Headers
		output_file.write("P3\n")
		output_file.write(f"{len(screen)} {len(screen[0])}\n")
		output_file.write(f"{max_color}\n")

		# Pixels
		pixel_coords = [(x,y) for y in range(len(screen[0])) for x in range(len(screen))]
		if progress_bar:
			pixel_coords = tqdm(pixel_coords)
		for x,y in pixel_coords:
			pixel = screen[x,y]*max_color
			output_file.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")


def write_to_png(screen: np.ndarray, output_file_path: str, progress_bar: bool):
	""" Writes the screen to a file with [PNG](https://en.wikipedia.org/wiki/PNG) encoding. """

	width = len(screen)
	height = len(screen[0])

	pixel_coords = [(x,y) for y in range(height) for x in range(width)]
	pixels = [tuple((screen[x,y] * max_color).astype(int)) for x,y in pixel_coords]

	image = Image.new('RGB', (width, height))
	image.putdata(pixels)
	image.save(output_file_path)
