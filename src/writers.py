import numpy as np

# TODO add support for other image types

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
