import argparse
import sys
import threading
import time
import json

from .IOTDevice import IOTDevice

class DummySensorDevice(IOTDevice):
	"""
	Class that represents a sensor device.
	"""
	def __init__(
		self,
		host: str,
		port: int,
		device_id: str,
		interval: float = 1.0,
		min_value: float = 20.0,
		max_value: float = 30.0,
		increment: float = 1.0
	):
		"""
		Constructor of the DummySensorDevice class.
		Args:
			host (str): Host of the MQTT broker.
			port (int): Port of the MQTT broker.
			device_id (str): ID of the device.
			min_value (float): Minimum value to send.
			max_value (float): Maximum value to send.
			increment (float): Increment between min and max.
		"""
		# Save the default device params
		super().__init__(
			host,
			port,
			device_id,
			self.on_connect,
			self.on_message
		)

		# Save the sensor params
		self.interval = interval
		self.min_value = min_value
		self.max_value = max_value
		self.increment = increment

		# Set the value to the min value
		self.value = min_value

		# Set the sensor header, so it can be used in the debug prints
		self.device_header = f"[Dummy Sensor - {self.device_id}]"

		# Possible commands
		self.commands = {
			'get': self.get_command,
		}

	def publish_status(self):
		"""
		Publish the status of the sensor.
		"""
		# Publish the state
		print(f"{self.device_header} Publishing state: {self.value}")
		self.client.publish(
			self.status_topic,
			json.dumps({
				"state": self.value,
			}),
			qos=1,
			retain=True,
		)

	def on_connect(self, client, userdata, flags, rc) -> None:
		"""
		Callback function that is called when the client connects to the broker.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata: The private user data as set in Client() or userdata_set.
			flags (dict): Response flags sent by the broker.
			rc (int): The connection result.
		"""
		# Debug print
		print(f"{self.device_header} Connected with result code {rc}")
		
		# Subscribe to the command topic
		print(f"{self.device_header} Init state: {self.value}")
		print(f"{self.device_header} Subscribing to {self.command_topic}", end="\n\n")
		self.client.subscribe(self.command_topic)

		# Publish the init state
		self.publish_status()

		# Create a thread that will be publishing the state
		thead = threading.Thread(
			target=self.device_loop,
			daemon=True
		)
		thead.start()

	def device_loop(self):
		"""
		Loop that publishes the state of the sensor.
		"""
		while True:
			# Wait the interval set
			time.sleep(self.interval)

			# Update the value:
			# If it is > max value or < min value, the increment is set to the opposite sign
			next_value = self.value + self.increment
			if next_value > self.max_value or next_value < self.min_value:
				self.increment = -self.increment
			self.value += self.increment

			# Publish the new state
			self.publish_status()


	def on_message(self, client, userdata, msg) -> None:
		"""
		Callback function that is called when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata: The private user data as set in Client() or userdata_set in subscribe().
			msg (mqtt.MQTTMessage): An instance of MQTTMessage.
		"""
		print(f"{self.device_header} Received message: {str(msg.payload.decode())}")
		try:
			payload = json.loads(msg.payload)
		except json.JSONDecodeError:
			print(f"{self.device_header} Bad message format")
			return

		# Check if a command has been received
		if 'cmd' not in payload:
			print(f"{self.device_header} Invalid message received, ignoring")
			return

		# Execute the command
		current_command = self.commands.get(payload['cmd'])
		if current_command:
			current_command(client, userdata, payload)
			return

		# Comamnd not valid
		print(f"{self.device_header} Invalid command received, ignoring")

	def get_command(self, client, userdata, payload) -> None:
		"""
		Command that is executed when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata: The private user data as set in Client() or userdata_set in subscribe().
			payload (Any): The payload of the message.
		"""
		print(f"{self.device_header} Status is {self.value}")
		self.publish_status()

def parse_params() -> argparse.Namespace:
	"""
	Parse the parameters of the script.
	Returns:
		argparse.Namespace: The parsed parameters.
	"""
	# Init the object
	params = argparse.ArgumentParser(
		description="IOT Dummy Sensor"
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
		"-i", "--interval", type=float, default=1.0,
		help="Time in seconds after which a change of state is simulated (default: %(default)s)"
	)
	params.add_argument(
		"-m", "--min", type=float, default=20.0,
		help="Minimum value to send (default: %(default)s)"
	)
	params.add_argument(
		"-M", "--max", type=float, default=30.0,
		help="Maximun value to send (default: %(default)s)"
	)
	params.add_argument(
		"--increment", type=float, default=1.0,
		help="Increment between min and max (default: %(default)s)"
	)
	params.add_argument(
		"id",
		help="IOT Device ID"
	)
	parsed = params.parse_args()

	# Added constraints
	if parsed.min > parsed.max:
		params.error("The min value must be less than the max value")

	# Return the params
	return parsed

def main():
	"""
	Main function of the script.
	"""
	# Parse the params
	args = parse_params()

	# Init sensor
	device = DummySensorDevice(
		host=args.host,
		port=args.port,
		device_id=args.id,
		interval=args.interval,
		min_value=args.min,
		max_value=args.max,
		increment=args.increment
	)

	# Run the device
	error = device.run()
	if error:
		print(f"Error during the execution: {error}")
		sys.exit(1)

if __name__ == "__main__":
	main()