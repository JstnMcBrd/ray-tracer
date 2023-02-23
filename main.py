import argparse
from dotenv import load_dotenv
from os import getenv

if __name__ == "__main__":
	load_dotenv()

	arg = argparse.ArgumentParser("CS 455 Ray Tracer")
	arg.add_argument("-s", "--scene", type=str, help="Path to the scene file", default=getenv('SCENE'))
	parsed = arg.parse_args()
	
	# Arguments
	scene = parsed.scene
	