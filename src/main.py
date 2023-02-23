import argparse
from dotenv import load_dotenv
import json
import numpy as np
from os import getenv

from SceneImporter import loadFromJson
from Scene import Scene


def loadScene(filePath: str) -> Scene:
	jsonFile = None
	try:
		jsonFile = open(filePath, "r")
	except Exception as err:
		print(f"\"{filePath}\" is not a valid path\n\t{err}")
		exit(1)

	jsonData = None
	try:
		jsonData = json.loads(jsonFile.read())
	except Exception as err:
		print(f"\"{filePath}\" is not a valid json file\n\t{err}")
		exit(1)

	scene = None
	try:
		scene = loadFromJson(jsonData)
	except AssertionError as err:
		print(f"\"{filePath}\" is improperly formatted\n\t{err}")
		exit(1)

	return scene

def writeToPPM(screen: np.ndarray, outputFilePath: str):
	outputFile = open(outputFilePath, "w")
	outputFile.write("P3\n")
	outputFile.write(f"{len(screen[0])} {len(screen)}\n")
	outputFile.write("255\n")
	for row in screen:
		for pixel in row:
			outputFile.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
		outputFile.write("\n")


def raytrace(scene: Scene, width: int, height: int) -> np.ndarray:
	screen = np.zeros((height, width, 3))

	return screen


if __name__ == "__main__":
	load_dotenv()

	arg = argparse.ArgumentParser("CS 455 Ray Tracer")
	arg.add_argument("-s", "--scene", type=str, help="Path to the scene file", default=getenv("SCENE"), required=getenv("SCENE") == None)
	arg.add_argument("-o", "--output", type=str, help="Path to the output file", default=getenv("OUTPUT"), required=getenv("OUTPUT") == None)
	arg.add_argument("-x", "--width", type=int, help="Width of the output image", default=getenv("WIDTH"), required=getenv("WIDTH") == None)
	arg.add_argument("-y", "--height", type=int, help="Height of the output image", default=getenv("HEIGHT"), required=getenv("HEIGHT") == None)
	parsed = arg.parse_args()
	
	# Arguments
	sceneFilePath = parsed.scene
	outputFilePath = parsed.output
	width = parsed.width
	height = parsed.height

	# Load Scene
	scene = loadScene(sceneFilePath)

	# Raytrace
	screen = raytrace(scene, width, height)

	# Write to file
	writeToPPM(screen, outputFilePath)
