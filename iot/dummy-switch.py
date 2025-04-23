import argparse

def parse_params():
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
	args = parse_params()
	print(args)

if __name__ == '__main__':
	main()