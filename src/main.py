import argparse
from dotenv import load_dotenv
import json
from os import getenv

from Scene import Scene


def loadScene(filePath):
	jsonFile = None
	try:
		jsonFile = open(filePath)
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
		scene = Scene.loadFromJson(jsonData)
	except Exception as err:
		print(f"\"{filePath}\" is improperly formatted\n\t{err}")
		exit(1)

	return scene


if __name__ == "__main__":
	load_dotenv()

	arg = argparse.ArgumentParser("CS 455 Ray Tracer")
	arg.add_argument("-s", "--scene", type=str, help="Path to the scene file", default=getenv('SCENE'), required=getenv('SCENE') == None)
	parsed = arg.parse_args()
	
	# Arguments
	sceneFilePath = parsed.scene
	scene = loadScene(sceneFilePath)
	