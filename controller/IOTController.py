from .device import Device
from .rule import Rule
from typing import List, Dict, Any
import paho.mqtt.client as mqtt

class IOTController:
	def __init__(
		self,
		mqtt_host: str,
		mqtt_port: int,
		devices: List[Device],
		rules: List[Rule]
	):
		# Save the params
		self.mqtt_host = mqtt_host
		self.mqtt_port = mqtt_port
		self.devices = devices
		self.rules = rules

		# Set the client and callbacks
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message


	def on_connect(self, client, userdata, flags, rc):
		"""
		Callback function that is called when the client connects to the broker.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (Any): The private user data as set in Client() or userdata_set().
			flags (dict): Response flags sent by the broker.
			rc (int): The connection result.
		"""
		# Connect on each device status topic
		for device in self.devices:
			client.subscribe(device.status_topic)
		print("[ Controller ] Starting...")


	def on_message(self, client, userdata, msg):
		"""
		Callback function that is called when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (Any): The private user data as set in Client() or userdata_set().
			msg (paho.mqtt.message.MQTTMessage): The message that was received.
		"""
		pass