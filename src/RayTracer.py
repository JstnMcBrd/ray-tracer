from math import tan
import numpy as np

from Scene import Object, Scene

def rayTrace(scene: Scene, width: int, height: int) -> np.ndarray:
	screen = np.zeros((width, height, 3)) # TODO this is time/space intensive - maybe calculate + write values gradually?

	# Get camera axes and positions
	cameraLookFrom = scene.cameraLookFrom
	cameraLookAt = scene.cameraLookAt
	cameraForward = scene.cameraForward()
	cameraUp = scene.cameraUp()
	cameraRight = scene.cameraRight()

	# Calculate screen sizes
	viewportSize = np.array([width, height])
	windowSize = calculateWindowSize(viewportSize, cameraLookAt, cameraLookFrom, scene.fieldOfView)

	# Save time by pre-calcuating constant values
	windowToViewportSizeRatio = windowSize/viewportSize
	halfWindowSize = windowSize/2
	rayOrigin = scene.cameraLookFrom

	# For each pixel on the screen...
	for x in range(len(screen)):
		for y in range(len(screen[x])):
			# Find the world point of the pixel
			viewportPoint = np.array([x, y])
			windowPoint = viewportToWindow(viewportPoint, windowToViewportSizeRatio, halfWindowSize)
			worldPoint = windowToWorld(windowPoint, cameraForward, cameraLookAt, cameraUp, cameraRight)

			# Find the direction the ray is pointing
			rayDirection = normalize(worldPoint - cameraLookFrom)

			# Find the closest object that intersects with the ray
			closestObject = None
			closestIntersection = None
			closestDistance = float("inf")
			closestDirection = None
			for obj in scene.objects:
				intersection = obj.rayIntersection(rayOrigin, rayDirection)
				if not type(intersection) is type(None):
					direction = cameraLookFrom - intersection
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


def calculateWindowSize(viewportSize: np.ndarray, cameraLookFrom: np.ndarray, cameraLookAt: np.ndarray, fieldOfView: float) -> np.ndarray:
	dist = cameraLookAt - cameraLookFrom
	dist_mag = np.sqrt(np.dot(dist,dist))
	x = dist_mag * tan(np.deg2rad(fieldOfView/2)) * 2
	y = x * viewportSize[1]/viewportSize[0]
	return np.array([x, y])


def viewportToWindow(viewportPoint: np.ndarray, windowToViewportSizeRatio: np.ndarray, halfWindowSize: np.ndarray) -> np.ndarray:
	windowPoint = viewportPoint * windowToViewportSizeRatio - halfWindowSize
	return np.array([windowPoint[0], windowPoint[1]*-1, 0]) # The -1 seems necessary to orient it correctly


def windowToWorld(windowPoint: np.ndarray, cameraLookAt: np.ndarray, cameraForward: np.ndarray, cameraUp: np.ndarray, cameraRight: np.ndarray) -> np.ndarray:
	return cameraLookAt + windowPoint[0]*cameraRight + windowPoint[1]*cameraUp + windowPoint[2]*cameraForward


def shading(scene: Scene, obj: Object, surfaceNormal: np.ndarray, viewDirection: np.ndarray) -> np.ndarray:
	NdotL = np.dot(surfaceNormal, scene.directionToLight)
	reflected = 2 * surfaceNormal * NdotL - scene.directionToLight

	ambient = obj.ambientCoefficient * scene.ambientLightColor * obj.diffuseColor
	diffuse = obj.diffuseCoefficient * scene.lightColor * obj.diffuseColor * max(0, NdotL)
	specular = obj.specularCoefficient * scene.lightColor * obj.specularColor * max(0, np.dot(viewDirection, reflected))**obj.glossCoefficient
	return ambient + diffuse + specular