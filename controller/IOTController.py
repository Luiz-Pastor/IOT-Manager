from .device import Device
from .rule import Rule
from typing import List, Dict, Any
import paho.mqtt.client as mqtt
import threading
import json
from .api_communication import add_log_message
from datetime import datetime

def get_correct_value(key: str, value: str) -> Any:
	"""
	Function to get the correct value of a variable.
	Args:
		key (str): The key of the variable.
		value (str): The value of the variable.
	Returns:
		The correct value of the variable.
	"""
	# Temperature
	if key == 'temperature':
		try:
			return float(value)
		except ValueError:
			raise ValueError("Invalid value for temperature")

	# Time
	if key == 'time':
		try:
			return datetime.strptime(value, '%H:%M:%S').time()
		except ValueError:
			raise ValueError("Invalid value for time")

	# State
	if key == 'state':
		if value != 'ON' and value != 'OFF':
			raise ValueError("Invalid value for state")
		return value

	raise ValueError("Invalid key")

def compare_values(
		value1: Any,
		value2: Any,
		operator: str
) -> bool:
	"""
	Function to compare two values.
	Args:
		value1 (Any): The first value.
		value2 (Any): The second value.
		operator (str): The operator to use for the comparison.
	Returns:
		The result of the comparison.
	"""
	oprs = {
		'>': lambda x, y: x > y,
		'<': lambda x, y: x < y,
		'==': lambda x, y: x == y,
		'!=': lambda x, y: x != y,
		'>=': lambda x, y: x >= y,
		'<=': lambda x, y: x <= y,
	}

	if operator in oprs:
		return oprs[operator](value1, value2)

	raise ValueError("Invalid operator")


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
		
		# Get the variable to check, and convert to the correct value
		key_to_check = device.state_variable
		value = payload.get(key_to_check)
		try:
			source_correct_value = get_correct_value(key_to_check, value)
		except ValueError:
			# TODO: Notify the server the error
			return

		# Check the rules, checking if it has to be applied
		for rule in self.rules:
			# Check if the rule matches the device
			if rule.source_device_id != device_id:
				continue

			# Convert the threshold to the correct value
			try:
				threshold = get_correct_value(key_to_check, rule.threshold)
			except ValueError:
				# TODO: Notify the server the error
				return
			
			# Make the comparation, and check if it is correct
			try:
				comparation = compare_values(source_correct_value, threshold, rule.operator)
			except ValueError:
				# TODO: Notify the server the error
				return
			
			if not comparation:
				continue

			# Execute the command on the target device (send the command payload)
			target_device = next(
				(device for device in self.devices if device.id == rule.target_device_id),
				None
			)
			if not target_device:
				continue
			self.client.publish(
				target_device.command_topic,
				rule.command_payload,
				qos=1
			)

			# Notify django
			add_log_message(
				self.server_host,
				self.server_port,
				f"Rule '{rule.name}' applied",
				device_id
			)