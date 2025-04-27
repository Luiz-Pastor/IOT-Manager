import argparse
import sys
import random
from enum import Enum
import json

from .IOTDevice import IOTDevice

class SwitchState(Enum):
	"""
	Enum class to represent the state of the switch.
	"""
	SWITCH_ON = "ON"
	SWITCH_OFF = "OFF"

class DummySwitchDevice(IOTDevice):
	"""
	Class that represents a switch device.
	"""
	def __init__(
		self,
		host: str,
		port: int,
		device_id: str,
		probability: float = 0.3
	):
		"""
		Constructor of the DummySwitchDevice class.
		Args:
			host (str): Host of the MQTT broker.
			port (int): Port of the MQTT broker.
			device_id (str): ID of the device.
			probability (float): Probability of the switch failing.
		"""
		# Save the main device params
		super().__init__(
			host,
			port,
			device_id,
			self.on_connect,
			self.on_message
		)

		# Save the switch probability
		self.probability = probability

		# Set the switch init state
		self.status = SwitchState.SWITCH_OFF

		# Device header, for debugging
		self.device_header = f"[Dummy witch - {self.device_id}]"
	
		# Possible commands
		self.commands = {
			'get': self.get_command,
			'set': self.set_command,
		}

	def publish_status(self) -> None:
		"""
		Publish the current status of the device.
		"""
		self.client.publish(
			self.status_topic,
			json.dumps({
				"state": self.status.value,
			}),
			qos=1,
			retain=True,
		)

	def on_connect(self, client, userdata, flags, rc) -> None:
		"""
		Callback function that is called when the client connects to the broker.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (any): The private user data as set in Client() or userdata_set().
			flags (dict): Response flags sent by the broker.
			rc (int): The connection result.
		"""
		# Debud print
		print(f"{self.device_header} Connected with result code {rc}")

		# Subscribe to the command topic
		print(f"{self.device_header} Init state: {self.status.value}")
		print(f"{self.device_header} Subscribing to {self.command_topic}", end="\n\n")
		self.client.subscribe(self.command_topic)

		# Publish the current state
		self.publish_status()

	def on_message(self, client, userdata, msg) -> None:
		"""
		Callback function that is called when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (any): The private user data as set in Client() or userdata_set.
			msg (mqtt.MQTTMessage): An instance of MQTTMessage. This is a class with
				two members: topic and payload. The payload is a bytes object and can
				be decoded by using the decode() method.
		"""
		# Get the message payload
		print(f"{self.device_header} Received message: {msg.payload.decode()}")
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
		Callback function that is called when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (any): The private user data as set in Client() or userdata_set().
			payload (json): The payload of the message, as JSON
		"""
		print(f"{self.device_header} Status is {self.status.value}")
		self.publish_status()
		
	def set_command(self, client, userdata, payload) -> None:
		"""
		Callback function that is called when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (any): The private user data as set in Client() or userdata_set().
			payload (json): The payload of the message, as JSON
		"""
		if 'state' not in payload:
			print(f"{self.device_header} Error: no state received")
			return

		# Get the status from the enum
		try:
			received_status = SwitchState(payload['state'])
		except ValueError:
			print(f"{self.device_header} Invalid state received, ignoring")
			received_status = None
		
		# If the status is valid, try to change it
		if received_status:
			random_number = random.randint(0, 100) / 100

			# Simulate a failure
			if received_status == self.status:
				print(f"{self.device_header} Status is already {self.status.value}")
			elif random_number < self.probability:
				print(f"{self.device_header} Simulating a failure")
			else:
				print(f"{self.device_header} Changing status from {self.status.value} to {received_status.value}")
				self.status = received_status
		
		# Publish the current state
		self.publish_status()

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
	device = DummySwitchDevice(
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