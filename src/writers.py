"""
Contains methods for writing the screen to image files.
"""


from typing import Iterable
import numpy as np
from PIL import Image
from tqdm import tqdm


def write_to_ppm(screen: np.ndarray, output_file_path: str, progress_bar: bool):
	""" Writes the screen to a file with [PPM](https://en.wikipedia.org/wiki/Netpbm) encoding. """

	width = len(screen)
	height = len(screen[0])
	max_color = 255

	screen = screen * max_color
	coords: Iterable = [(x,y) for y in range(height) for x in range(width)]
	if progress_bar:
		coords = tqdm(coords)

	with open(output_file_path, mode="w", encoding="utf8") as output_file:
		# Headers
		output_file.write("P3\n")
		output_file.write(f"{width} {height}\n")
		output_file.write(f"{max_color}\n")

		# Pixels
		for x,y in coords:
			pixel = screen[x,y]
			output_file.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")


def write_to_png(screen: np.ndarray, output_file_path: str, progress_bar: bool):
	""" Writes the screen to a file with [PNG](https://en.wikipedia.org/wiki/PNG) encoding. """

	width = len(screen)
	height = len(screen[0])

	screen = (screen * 255).astype(int)
	coords: Iterable = [(x,y) for y in range(height) for x in range(width)]

	image = Image.new('RGB', (width, height))
	for xy in coords:
		image.putpixel(xy, tuple(screen[xy]))
	image.save(output_file_path)
