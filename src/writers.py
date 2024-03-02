"""
Contains methods for writing the screen to image files.
"""


from typing import Iterable
import numpy as np
from PIL import Image
from tqdm import tqdm


def write_to_png(screen: np.ndarray, output_file_path: str, progress_bar: bool):
	""" Writes the screen to a file with [PNG](https://en.wikipedia.org/wiki/PNG) encoding. """

	width = len(screen)
	height = len(screen[0])

	screen = (screen * 255).astype(int)
	coords: Iterable = [(x,y) for y in range(height) for x in range(width)]
	if progress_bar:
		coords = tqdm(coords)

	image = Image.new('RGB', (width, height))
	for xy in coords:
		r, g, b = screen[xy]
		image.putpixel(xy, (r, g, b))
	image.save(output_file_path)
