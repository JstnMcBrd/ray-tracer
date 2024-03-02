"""
Contains methods for writing the screen to image files.
"""


from os import remove
import sys

import numpy as np
from PIL import Image


def assert_supported_extension(output_file_path: str) -> None:
	""" Checks whether the file path with the given extension is supported by Pillow. """
	try:
		Image.new('RGB', (1, 1)).save(output_file_path)
		remove(output_file_path)
	except ValueError:
		extension = output_file_path.split(".")[-1]
		print(f"Output file extension is not supported: {extension}")
		sys.exit(1)


def export(screen: np.ndarray, output_file_path: str) -> None:
	""" Writes the screen to a file using the encoding of the file extension. """

	width = len(screen)
	height = len(screen[0])

	screen = (screen * 255).astype(np.uint8)

	# pylint: disable-next=fixme
	# FIXME making up for the screen being indexed by [col, row] instead of [row, col]
	screen = np.array(Image.fromarray(screen).rotate(-90))

	screen.resize((width * height, 3))
	data: list = [tuple(pixel) for pixel in screen]

	image = Image.new('RGB', (width, height))
	image.putdata(data)
	image.save(output_file_path)
