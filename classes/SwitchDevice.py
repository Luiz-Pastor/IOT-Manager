from .IOTDevice import IOTDevice
import random
from enum import Enum

class SwitchState(Enum):
	"""
	Enum class to represent the state of the switch.
	"""
	PAYLOAD_ON = "ON"
	PAYLOAD_OFF = "OFF"

class SwitchDevice(IOTDevice):
	"""
	Class that represents a switch device.
	"""
	def __init__(self, host, port, device_id, probability=0.3):
		"""
		Constructor of the SwitchDevice class.
		Args:
			host (str): Host of the MQTT broker.
			port (str): Port of the MQTT broker.
			device_id (str): ID of the device.
		"""
		# Save the main device params
		super().__init__(host, port, device_id)

		# Save the switch probability
		self.probability = probability

		# Set the switch init state
		self.status = SwitchState.PAYLOAD_OFF

		# Set the function
		self.client.on_message = self.on_message
		self.client.on_connect = self.on_connect

		# Device header, for debugging
		self.device_header = f"[Switch - {self.device_id}]"
	
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
		self.client.subscribe(self.command_topic)

		# Publish the current state
		self.client.publish(
			self.status_topic,
			self.status.value,
		)

	def on_message(self, client, userdata, msg):
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
		payload = msg.payload.decode().strip().upper()
		print(f"{self.device_header} Received message: {payload}")

		# Get the status from the enum
		try:
			received_status = SwitchState(payload)
		except ValueError:
			print(f"{self.device_header} Invalid status received, ignoring")
			received_status = None
		
		# If the status is valid, try to change it
		if received_status:
			random_number = random.randint(0, 100) / 100

			# Simulate a failure
			if random_number < self.probability:
				print(f"{self.device_header} Simulating a failure")
			elif received_status == self.status:
				print(f"{self.device_header} Status is already {self.status.value}")
			else:
				print(f"{self.device_header} Changing status from {self.status.value} to {received_status.value}")
				self.status = received_status
		
		# Publish the current state
		self.client.publish(
			self.status_topic,
			self.status.value,
		)
