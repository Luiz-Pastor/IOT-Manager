import argparse
import sys
from typing import Optional
from datetime import datetime, timedelta
import threading
import time
import json

from .IOTDevice import IOTDevice

DEBUG_MODE = None

class DummyClockDevice(IOTDevice):
	"""
	Class that represents a clock device.
	"""
	def __init__(
		self,
		host: str,
		port: int,
		device_id: str,
		start_time: Optional[str] = None,
		increment: int = 1,
		rate: float = 1.0
	):
		"""
		Constructor of the DummyClockDevice class.
		Args:
			host (str): Host of the MQTT broker.
			port (int): Port of the MQTT broker.
			device_id (str): ID of the device.
			start_time (str): Time to start from, in HH:MM:SS format.
			increment (int): Increment between shipments in seconds.
			rate (float): Sending frequency in seconds.
		"""
		# Save the default device params
		super().__init__(
			host,
			port,
			device_id,
			self.on_connect,
			self.on_message
		)

		# Save the clock params
		self.increment = increment
		self.rate = rate

		# Parse the time (current_time)
		now_time = datetime.now()
		if not start_time:
			self.current_time = now_time
		else:
			hours, minutes, seconds = map(int, start_time.split(':'))
			self.current_time = datetime.combine(
				now_time.date(), datetime.min.time()
			).replace(hour=hours, minute=minutes, second=seconds)

		# Device header, so it can be used in the debug prints
		self.device_header = f"[Dummy Clock - {self.device_id}]"

		# Possible commands
		self.commands = {
			'get': self.get_command,
		}

	
	def publish_state(self):
		"""
		Publish the state of the sensor.
		"""
		# Publish the state
		time_str = self.current_time.strftime("%H:%M:%S")
		if DEBUG_MODE:
			print(f"{self.device_header} Publishing state: {time_str}")
		self.client.publish(
			self.state_topic,
			json.dumps({
				"time": time_str,
			}),
			qos=1,
			retain=True
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
		if DEBUG_MODE:
			# Debug that the connection has been established
			print(f"{self.device_header} Connected with result code {rc}")

			# Subscribe to the command topic
			print(f"{self.device_header} Init state: {self.current_time.strftime('%H:%M:%S')}")
			print(f"{self.device_header} Subscribing to {self.command_topic}", end="\n\n")
		self.client.subscribe(self.command_topic)

		# Publish the init state
		self.publish_state()

		# Create a thread that will be publishing the state
		thread = threading.Thread(
			target=self.publish_time_loop,
			daemon=True
		)
		thread.start()

	def publish_time_loop(self) -> None:
		"""
		Loop that publishes the time every self.rate seconds.
		"""
		# Calculate the time to wait
		time_to_wait = 1.0 / self.rate

		# Loop where the info is sent
		while True:
			# Sleep the calculated time
			time.sleep(time_to_wait)

			# Update the time
			self.current_time += timedelta(seconds=self.increment)

			# Publish the state
			self.publish_state()

	def on_message(self, client, userdata, msg) -> None:
		"""
		Callback function that is called when a message is received from the broker.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata: The private user data as set in Client() or userdata_set.
			msg (mqtt.MQTTMessage): An instance of MQTTMessage.
		"""
		if DEBUG_MODE:
			print(f"{self.device_header} Received message: {str(msg.payload.decode())}")
		try:
			payload = json.loads(msg.payload)
		except json.JSONDecodeError:
			if DEBUG_MODE:
				print(f"{self.device_header} Bad message format")
			return

		# Check if a command has been received
		if 'cmd' not in payload:
			if DEBUG_MODE:
				print(f"{self.device_header} Invalid message received, ignoring")
			return

		# Execute the command
		current_command = self.commands.get(payload['cmd'])
		if current_command:
			current_command(client, userdata, payload)
			return

		# Comamnd not valid
		if DEBUG_MODE:
			print(f"{self.device_header} Invalid command received, ignoring")

	def get_command(self, client, userdata, payload: str) -> None:
		"""
		Command that is executed when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata: The private user data as set in Client() or userdata_set in subscribe().
			payload (Any): The payload of the message.
		"""
		if DEBUG_MODE:
			print(f"{self.device_header} state is {self.current_time.strftime('%H:%M:%S')}")
		self.publish_state()


def parse_params() -> argparse.Namespace:
	"""
	Parse the parameters of the script.
	Returns:
		argparse.Namespace: The parsed parameters.
	"""
	# Init the object
	params = argparse.ArgumentParser(
		description="IOT Dummy Watch"
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
		"--time", dest='start_time', default=None,
		help="Start time, from which it starts (default: %(default)s)"
	)
	params.add_argument(
		"--increment", type=int, default=1,
		help="Increment between shipments in seconds (default: %(default)s)"
	)
	params.add_argument(
		"--rate", type=float, default=1.0,
		help="Sent messages per second (default: %(default)s)"
	)
	params.add_argument(
		"--debug", type=bool, default=False,
		help="Debug mode (default: %(default)s)"
	)
	params.add_argument(
		"id",
		help="IOT Device ID"
	)
	parsed = params.parse_args()

	# Added constraints
	if parsed.increment <= 0:
		params.error("The increment value must be greater than 0")

	if parsed.rate <= 0:
		params.error("The rate value must be greater than 0")

	if parsed.start_time:
		parts = parsed.start_time.split(':')
		if len(parts) != 3 or not all(part.isdigit() for part in parts):
			params.error("The time format must be HH:MM:SS")

	# Return the params
	return parsed

def main():
	"""
	Main function of the script.
	"""
	global DEBUG_MODE

	# Parse the params
	args = parse_params()
	DEBUG_MODE = args.debug

	# Init sensor
	device = DummyClockDevice(
		host=args.host,
		port=args.port,
		device_id=args.id,
		start_time=args.start_time,
		increment=args.increment,
		rate=args.rate
	)

	# Simulate clock
	error = device.run()
	if error:
		if DEBUG_MODE:
			print(f"Error during the execution: {error}")
		sys.exit(1)
	
if __name__ == "__main__":
	main()