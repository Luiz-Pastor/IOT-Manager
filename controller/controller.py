import sys
import argparse
from typing import Union, Tuple, List
from .device import Device
from .rule import Rule
from .IOTController import IOTController
from .database_communication import check_database

def parse_params() -> argparse.Namespace:
	"""
	Parse the parameters of the script.
	Returns:
		argparse.Namespace: The parsed parameters.
	"""
	# Init the object
	params = argparse.ArgumentParser(
		description="IOT Controller"
	)

	# Add the params
	params.add_argument(
		"--host", default="redes2.ii.uam.es",
		help="Host of the MQTT broker (default: %(default)s)"
	)
	params.add_argument(
		"--port", type=int, default=1883,
		help="Port of the MQTT broker (default: %(default)s)"
	)
	params.add_argument(
		"-db", "--database", default="../iot-manager/db.sqlite3",
		help="IOT Database (default: %(default)s)"
	)
	params.add_argument(
		"--debug", type=bool, default=False,
		help="Debug mode (default: %(default)s)"
	)
	parsed = params.parse_args()

	# Return the params
	return parsed

def main():
	"""
	Main function of the script.
	"""
	# Parse the params
	args = parse_params()

	# Check if the database exists
	if not check_database(args.database):
		print(f"[ Controller ] Database {args.database} not found.")
		sys.exit(1)

	# Create the controller, and run it
	controller = IOTController(
		host=args.host,
		port=args.port,
		database=args.database,
		debug=args.debug
	)
	controller.start()

	# Loop until a SIGINT is received
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("[ Controller ] Stopping...")


if __name__ == '__main__':
	main()
