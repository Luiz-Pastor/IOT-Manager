import argparse
from ..classes import SwitchDevice
import sys

def parse_params() -> argparse.Namespace:
	"""
	Parse the parameters of the script.
	Returns:
		argparse.Namespace: The parsed parameters.
	"""
	# Init the object
	params = argparse.ArgumentParser(
		description="IOT Switch"
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
		"-P", "--probability", type=float, default=0.3,
		help="Probability of failure when changing state (default: %(default)s)"
	)
	params.add_argument(
		"id",
		help="IOT Device ID"
	)
	parsed = params.parse_args()

	# Add constraints
	if parsed.probability < 0 or parsed.probability > 1:
		params.error("The probability must be between 0 and 1, both inclusive.")
	
	# Return the params
	return parsed

def main():
	"""
	Main function of the script.
	"""
	# Parse the params
	args = parse_params()

	# Init switch
	device = SwitchDevice(
		host=args.host,
		port=args.port,
		device_id=args.id,
		probability=args.probability
	)

	# Run the device
	error = device.run()
	if error:
		print(f"Error during the execution: {error}")
		sys.exit(1)

if __name__ == '__main__':
	main()