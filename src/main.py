import argparse
from dotenv import load_dotenv
import json
from math import tan
import numpy as np
from os import getenv

from SceneImporter import loadFromJson
from Scene import Scene, Sphere


# TODO shadows
# TODO reflection
# TODO refraction
# TODO more than one light source


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


def writeToPPM(screen: np.ndarray, outputFilePath: str, maxColor: float):
	outputFile = open(outputFilePath, "w")
	outputFile.write("P3\n")
	outputFile.write(f"{len(screen)} {len(screen[0])}\n")
	outputFile.write(f"{maxColor}\n")
	for y in range(len(screen[0])):
		for x in range(len(screen)):
			pixel = screen[x,y]*maxColor
			outputFile.write(f"{pixel[0]} {pixel[1]} {pixel[2]}     ")
		outputFile.write("\n")


def raytrace(scene: Scene, width: int, height: int) -> np.ndarray:
	screen = np.zeros((width, height, 3))

	# Calculate screen sizes
	viewportSize = np.array([width, height])
	windowSize = calculateWindowSize(viewportSize, scene.cameraLookAt, scene.cameraLookFrom, scene.fieldOfView)

	# Save time by pre-calcuating constant values
	windowViewportSizeRatio = windowSize/viewportSize
	halfWindowSize = windowSize/2
	rayOrigin = scene.cameraLookFrom

	# Get camera axises
	cameraForward = scene.cameraForward()
	cameraUp = scene.cameraUp()
	cameraRight = scene.cameraRight()

	# For each pixel on the screen...
	for x in range(len(screen)):
		for y in range(len(screen[x])):
			# Find the world point of the pixel
			viewportPoint = np.array([x, y])
			windowPoint = viewportToWindow(viewportPoint, windowViewportSizeRatio, halfWindowSize)
			worldPoint = windowToWorld(windowPoint, cameraForward, cameraUp, cameraRight)

			# Find the direction the ray is pointing
			rayDirection = normalize(worldPoint - scene.cameraLookFrom)

			# Find the closest object that intersects with the ray
			closestObject = None
			closestIntersection = None
			closestDistance = float("inf")
			closestDirection = None
			for obj in scene.objects:
				intersection = obj.rayIntersection(rayOrigin, rayDirection)
				if not type(intersection) is type(None):
					direction = scene.cameraLookFrom - intersection
					distance = magnitude(direction)
					if distance < closestDistance:
						closestObject = obj
						closestIntersection = intersection
						closestDistance = distance
						closestDirection = direction

			# Shade the pixel using the closest object
			if closestObject != None:
				viewDirection = closestDirection / closestDistance
				normal = closestObject.normal(closestIntersection)
				screen[x,y] = shading(scene, closestObject, normal, viewDirection)
			
			# If no object collided, use the background
			else:
				screen[x,y] = scene.backgroundColor

	return screen


def magnitude(vector: np.ndarray) -> float:
	return np.sqrt(np.dot(vector,vector))


def normalize(vector: np.ndarray) -> np.ndarray:
	return vector / magnitude(vector)


def calculateWindowSize(viewportSize: np.ndarray, cameraLookAt: np.ndarray, cameraLookFrom: np.ndarray, fieldOfView: float) -> np.ndarray:
	dist = cameraLookAt - cameraLookFrom
	dist_mag = np.sqrt(np.dot(dist,dist))
	x = dist_mag * tan(np.deg2rad(fieldOfView/2)) * 2
	y = x * viewportSize[1]/viewportSize[0]
	return np.array([x, y])


def viewportToWindow(viewportPoint: np.ndarray, windowViewportSizeRatio: np.ndarray, halfWindowSize: np.ndarray) -> np.ndarray:
	windowPoint = viewportPoint * windowViewportSizeRatio - halfWindowSize
	return np.array([windowPoint[0], windowPoint[1]*-1, 0]) # The -1 seems necessary to orient it correctly


def windowToWorld(windowPoint: np.ndarray, cameraForward: np.ndarray, cameraUp: np.ndarray, cameraRight: np.ndarray) -> np.ndarray:
	return scene.cameraLookAt + windowPoint[0]*cameraRight + windowPoint[1]*cameraUp + windowPoint[2]*cameraForward


def shading(scene: Scene, obj: Sphere, surfaceNormal: np.ndarray, viewDirection: np.ndarray) -> np.ndarray:
	NdotL = np.dot(surfaceNormal, scene.directionToLight)
	reflected = 2 * surfaceNormal * NdotL - scene.directionToLight

	ambient = obj.ambientCoefficient * scene.ambientLightColor * obj.diffuseColor
	diffuse = obj.diffuseCoefficient * scene.lightColor * obj.diffuseColor * max(0, NdotL)
	specular = obj.specularCoefficient * scene.lightColor * obj.specularColor * max(0, np.dot(viewDirection, reflected))**obj.glossCoefficient
	return ambient + diffuse + specular

if __name__ == "__main__":
	load_dotenv()

	arg = argparse.ArgumentParser("CS 455 Ray Tracer")
	arg.add_argument("-s", "--scene", type=str, help="Path to the scene file", default=getenv("SCENE"), required=getenv("SCENE") == None)
	arg.add_argument("-o", "--output", type=str, help="Path to the output file", default=getenv("OUTPUT"), required=getenv("OUTPUT") == None)
	arg.add_argument("-x", "--width", type=int, help="Width of the output image", default=getenv("WIDTH"), required=getenv("WIDTH") == None)
	arg.add_argument("-y", "--height", type=int, help="Height of the output image", default=getenv("HEIGHT"), required=getenv("HEIGHT") == None)
	arg.add_argument("-c", "--max-color", type=float, help="The maximum color of the ppm file", default=getenv("MAX_COLOR", default=255), required=getenv("MAX_COLOR", default=255) == None)
	parsed = arg.parse_args()
	
	# Arguments
	sceneFilePath = parsed.scene
	outputFilePath = parsed.output
	width = parsed.width
	height = parsed.height
	maxColor = parsed.max_color

	# Load Scene
	scene = loadScene(sceneFilePath)

	# Raytrace
	screen = raytrace(scene, width, height)

	# Write to file
	writeToPPM(screen, outputFilePath, maxColor)
