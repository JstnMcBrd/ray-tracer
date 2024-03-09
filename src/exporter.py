"Contains methods for writing the screen to image files."


import sys
from pathlib import Path
from secrets import choice
from string import ascii_letters

import numpy as np
from numpy.typing import NDArray
from PIL import Image


COLOR_MODE = 'RGB'


def random_str(length: int) -> str:
	"Generates a random string of the given length."

	return ''.join(choice(ascii_letters) for _ in range(length))


def assert_supported_extension(output_file_path: str) -> None:
	"Asserts that the file path with the given extension is supported by Pillow."

	extension = output_file_path.split(".")[-1]
	random_file_name = f"temp_{random_str(10)}.{extension}"
	try:
		Image.new(COLOR_MODE, (1, 1)).save(random_file_name)
		remove(random_file_name)
	except ValueError:
		print(f"Output file extension is not supported: {extension}")
		sys.exit(1)


	"Writes the screen to a file using the encoding of the file extension."

def export(screen: NDArray[np.float64], output_file_path: str) -> None:
	height, width, depth = screen.shape

	screen = (screen * 255).astype(np.uint8)
	screen.resize(width * height, depth)
	data: list = [tuple(pixel) for pixel in screen]

	image = Image.new(COLOR_MODE, (width, height))
	image.putdata(data)
	image.save(output_file_path)
