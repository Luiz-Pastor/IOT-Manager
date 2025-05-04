import sys
import argparse
from typing import Union, Tuple, List
from .device import Device
from .rule import Rule
from .IOTController import IOTController
from .api_communication import (
	get_devices_from_api,
	get_rules_from_api
)

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
		"-sh", "--server-host", default="http://localhost",
		help="Host of the Django (main) server (default: %(default)s)"
	)
	params.add_argument(
		"-sp", "--server-port", type=int, default=8000,
		help="Port of the Django server (default: %(default)s)"
	)
	parsed = params.parse_args()

	# Return the params
	return parsed

def load_devices(
		host: str,
		port: int
) -> Tuple[Union[str, List[Device]], bool]:
	"""
	Function to load the devices from the API.
	Args:
		host (str): Host of the Django server.
		port (int): Port of the Django server.
	Returns:
		The devices loaded from the API.
		The second parameter indicates if the devices were loaded correctly:
		if True, the first parameter is a list of devices
		if False, the first parameter is a string with the error message.
	"""
	# Get the devices from the API
	devices_data = get_devices_from_api(host, port)
	if devices_data is None:
		return "Error connecting with the server", False

	# Parse de API data
	devices = Device.from_api(devices_data)
	if devices is None:
		return "Error: unexpected structure of the API response", False
	
	# Return the correct data
	return devices, True

def load_rules(
		host: str,
		port: int
) -> Tuple[Union[str, List[Rule]], bool]:
	"""
	Function to load the rules from the API.
	Args:
		host (str): Host of the Django server.
		port (int): Port of the Django server.
	Returns:
		The rules loaded from the API.
		The second parameter indicates if the rules were loaded correctly:
		if True, the first parameter is a list of rules
		if False, the first parameter is a string with the error message.
	"""
	# Get the rules from the API
	rules_data = get_rules_from_api(host, port)
	if rules_data is None:
		return "Error connecting with the server", False

	# Parse de API data
	rules = Rule.from_api(rules_data)
	if rules is None:
		return "Error: unexpected structure of the API response", False

	# Return the correct data
	return rules, True

def main():
	"""
	Main function of the script.
	"""
	# Parse the params
	args = parse_params()

	# Load the devices
	devices, correct = load_devices(args.server_host, args.server_port)
	if not correct:
		print(devices)
		sys.exit(1)

	# Load the rules
	rules, correct = load_rules(args.server_host, args.server_port)
	if not correct:
		print(rules)
		sys.exit(1)

	# Create the controller, and run it
	controller = IOTController(
		mqtt_host=args.host,
		mqtt_port=args.port,
		server_host=args.server_host,
		server_port=args.server_port,
		devices=devices,
		rules=rules
	)
	controller.start()

	# TODO: Wait messages from the django (user)

	# Loop until a SIGINT is received
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("[ Controller ] Stopping...")


if __name__ == '__main__':
	main()
