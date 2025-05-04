from .device import Device
from .rule import Rule
from typing import List, Dict, Any
import paho.mqtt.client as mqtt
import threading
import json
from .api_communication import add_log_message

class IOTController:
	def __init__(
		self,
		mqtt_host: str,
		mqtt_port: int,
		server_host: str,
		server_port: int,
		devices: List[Device],
		rules: List[Rule]
	):
		# Save the params
		self.mqtt_host = mqtt_host
		self.mqtt_port = mqtt_port
		self.server_host = server_host
		self.server_port = server_port
		self.devices = devices
		self.rules = rules

		# Set the client and callbacks
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message

	def start(self) -> None:
		"""
		Connect to the MQTT broker and start the loop.
		"""
		# Connect to the broker
		self.client.connect(
			self.mqtt_host,
			self.mqtt_port,
		)

		# Execute, in a thread, the loop, so the main one can be still being used
		thread = threading.Thread(
			target=self.client.loop_forever,
			daemon=True
		)
		thread.start()

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
		# Get the device id that sent the message, and the device of the list
		device_id = msg.topic.split("/")[-2]
		device = next(
			(device for device in self.devices if device.id == device_id),
			None
		)
		if device is None:
			return

		# Get the payload and the topic
		try:
			payload = json.loads(msg.payload.decode())
		except json.JSONDecodeError:
			add_log_message(
				self.server_host,
				self.server_port,
				"Bad message format",
				device_id
			)
		
		# TODO: Check the rules
		# 	1. Get the variable to check
		#	2. Convert it to a type so it can be compared
		# 	3. Check the rules, and get all the ones that matches
		# 	4. Execute the rule, notifying django and sendking the command_payloads

		
		

			