import paho.mqtt.client as mqtt
from typing import Optional
from time import sleep

class IOTDevice:

	TOPIC_BASENAME = 'redes/2312/10'

	def __init__(self, host, password, devide_id):
		"""
		Constructor of the IOTDevice class.
		Args:
			host (str): Host of the MQTT broker.
			password (str): Password of the MQTT broker.
			devide_id (str): ID of the device.
		"""
		# Save the connections params
		self.host = host
		self.password = password

		# Save the device id
		self.device_id = devide_id

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
				keep_alive=60
			)
		except Exception as e:
			return str(e)

		# Start the loop and wait a keyboard interrupt
		try:
			self.client.loop_forever()
		except KeyboardInterrupt:
			self.client.disconnect()
		return None