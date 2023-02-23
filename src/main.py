import argparse
from dotenv import load_dotenv
import json
from math import tan
import numpy as np
from os import getenv

from SceneImporter import loadFromJson
from Scene import Scene, Sphere


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
	outputFile.write(f"{len(screen)} {len(screen[0])}\n")
	outputFile.write("1\n")
	for y in range(len(screen[0])):
		for x in range(len(screen)):
			pixel = screen[x,y]
			outputFile.write(f"{pixel[0]} {pixel[1]} {pixel[2]}     ")
		outputFile.write("\n")


def raytrace(scene: Scene, width: int, height: int) -> np.ndarray:
	screen = np.zeros((width, height, 3))
	viewportSize = np.array([width, height])
	windowSize = calculateWindowSize(viewportSize, scene.cameraLookAt, scene.cameraLookFrom, scene.fieldOfView)

	for x in range(len(screen)):
		for y in range(len(screen[x])):
			viewportPoint = np.array([x, y])
			windowPoint = viewportToWindow(viewportPoint, viewportSize, windowSize)
			worldPoint = windowToWorld(windowPoint, scene.cameraForward(), scene.cameraUp(), scene.cameraRight())

			rayOrigin = scene.cameraLookFrom
			rayDirection = worldPoint - scene.cameraLookFrom
			rayDirection /= np.sqrt(np.dot(rayDirection,rayDirection)) # normalize

			for obj in scene.objects:
				if type(obj) is Sphere:
					intersection = raySphereIntersection(rayOrigin, rayDirection, obj)
					if not type(intersection) is type(None):
						screen[x,y] = obj.color()

	return screen


def calculateWindowSize(viewportSize: np.ndarray, cameraLookAt: np.ndarray, cameraLookFrom: np.ndarray, fieldOfView: float) -> np.ndarray:
	dist = cameraLookAt - cameraLookFrom
	dist_mag = np.sqrt(np.dot(dist,dist))
	x = dist_mag * tan(np.deg2rad(fieldOfView/2)) * 2
	y = x * viewportSize[1]/viewportSize[0]
	return np.array([x, y])


def viewportToWindow(viewportPoint: np.ndarray, viewportSize: np.ndarray, windowSize: np.ndarray) -> np.ndarray:
	windowPoint = viewportPoint * windowSize/viewportSize - windowSize/2
	return np.array([windowPoint[0], windowPoint[1]*-1, 0]) # The -1 seems necessary to orient it correctly


def windowToWorld(windowPoint: np.ndarray, cameraForward: np.ndarray, cameraUp: np.ndarray, cameraRight: np.ndarray) -> np.ndarray:
	return scene.cameraLookAt + windowPoint[0]*cameraRight + windowPoint[1]*cameraUp + windowPoint[2]*cameraForward


def raySphereIntersection(rayOrigin: np.ndarray, rayDirection: np.ndarray, sphere: Sphere):
	dist = sphere.center - rayOrigin
	dist_sqr = np.dot(dist, dist)
	dist_mag = np.sqrt(dist_sqr)

	outside = dist_mag >= sphere.radius

	closestApproach = np.dot(rayDirection, dist)

	if closestApproach < 0 and outside:
		return None

	closestApproachDistToSurface_sqr = sphere.radius**2 - dist_sqr + closestApproach**2

	if closestApproachDistToSurface_sqr < 0:
		return None
	
	closestApproachDistToSurface = closestApproachDistToSurface_sqr**0.5

	t = closestApproach - closestApproachDistToSurface if outside else closestApproach + closestApproachDistToSurface

	return rayOrigin + rayDirection*t


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
