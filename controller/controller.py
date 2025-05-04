import argparse
from .api_communication import get_devices_from_api
from .device import Device

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

def main():
	"""
	Main function of the script.
	"""
	# Parse the params
	args = parse_params()

	# Load the devices
	devices_data = get_devices_from_api(args.server_host, args.server_port)
	devices = Device.from_api(devices_data)

if __name__ == '__main__':
	main()
