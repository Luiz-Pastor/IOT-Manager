import paho.mqtt.client as mqtt
from typing import Optional, Callable
from abc import ABC, abstractmethod

class IOTDevice(ABC):

	TOPIC_BASENAME = 'redes/2312/10'

	def __init__(
		self,
		host: str,
		port: int,
		device_id: str,
		on_connect: Callable,
		on_message: Callable
	):
		"""
		Constructor of the IOTDevice class.
		Args:
			host (str): Host of the MQTT broker.
			port (int): Port of the MQTT broker.
			device_id (str): ID of the device.
		"""
		# Save the connections params
		self.host = host
		self.port = port

		# Save the device id
		self.device_id = device_id

		# Save the topics that will be used
		self.state_topic = f"{self.TOPIC_BASENAME}/{self.device_id}/state"
		self.command_topic = f"{self.TOPIC_BASENAME}/{self.device_id}/command"

		# Create the client
		self.client = mqtt.Client(client_id=self.device_id)

		# Set the callbacks
		self.client.on_connect = on_connect
		self.client.on_message = on_message

	def run(self) -> Optional[str]:
		"""
		Connect with the broker and start the loop.
		Returns:
			str: The error str if it occurs, None otherwise.
		"""
		# Connect to the broker
		try:
			self.client.connect(
				self.host,
				self.port,
			)
		except Exception as e:
			return str(e)

		# Start the loop and wait a keyboard interrupt
		try:
			self.client.loop_forever()
		except KeyboardInterrupt:
			self.client.disconnect()
		return None

	@abstractmethod
	def on_connect(self, client, userdata, flags, rc) -> None:
		"""
		Callback function that is called when the client connects to the broker.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (any): The private user data as set in Client() or userdata_set().
			flags (dict): Response flags sent by the broker.
			rc (int): The connection result.
		"""
		pass

	@abstractmethod
	def on_message(self, client, userdata, msg) -> None:
		"""
		Callback function that is called when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (any): The private user data as set in Client() or userdata_set().
			msg (mqtt.MQTTMessage): An instance of MQTTMessage.
		"""
		pass

	@abstractmethod
	def publish_state(self) -> None:
		"""
		Publish the current state of the device.
		"""
		pass