import paho.mqtt.client as mqtt
from typing import Optional

class IOTDevice:

	TOPIC_BASENAME = 'redes/2312/10'

	def __init__(
		self,
		host: str,
		port: int,
		device_id: str
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
		self.status_topic = f"{self.TOPIC_BASENAME}/{self.device_id}"
		self.command_topic = f"{self.TOPIC_BASENAME}/{self.device_id}/command"

		# Create the client
		self.client = mqtt.Client(client_id=self.device_id)

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