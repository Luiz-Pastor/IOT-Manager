import argparse
from enum import Enum

class SwitchState(Enum):
	"""
	Enum class to represent the state of the switch.
	"""
	PAYLOAD_ON = "ON"
	PAYLOAD_OFF = "OFF"


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

	# Init switch state
	switch_state = SwitchState.PAYLOAD_OFF

	# Topics that the device will have
	topic = f"redes2/2312/10/{args.id}"				# Get the state
	command_topic = f"redes2/2312/10/{args.id}/set"	# Define state

if __name__ == '__main__':
	main()