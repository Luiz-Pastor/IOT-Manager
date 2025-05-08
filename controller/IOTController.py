from .device import Device
from .rule import Rule
from typing import List, Dict, Any
import paho.mqtt.client as mqtt
import threading
import json
from .database_communication import (
	create_connection,
	get_rules,
	add_log
)
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
		host: str,
		port: int,
		database: str,
		debug: bool = False
	):
		# Save the params
		self.mqtt_host = host
		self.mqtt_port = port
		self.database = database
		self.debug = debug


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
		if self.debug:
			print(f"[ Controller ] Connected to the broker with result code {rc}")
		self.client.subscribe("redes/2312/10/+/state")
		if self.debug:
			print("[ Controller ] Starting...")

	def on_message(self, client, userdata, msg):
		"""
		Callback function that is called when a message is received.
		Args:
			client (mqtt.Client): The client instance for this callback.
			userdata (Any): The private user data as set in Client() or userdata_set().
			msg (paho.mqtt.message.MQTTMessage): The message that was received.
		"""
		# Connect with the database
		database_connection = create_connection(self.database)

		# Get the device id that sent the message, and the device of the list
		device_id = msg.topic.split("/")[-2]
		if self.debug:
			print(f"[ {device_id} ] Message received from {device_id}")

		# Get the payload and the topic
		try:
			payload = json.loads(msg.payload.decode())
		except json.JSONDecodeError:
			add_log(
				database_connection,
				"Bad message format",
				device_id
			)
		if self.debug:
			print(f"[ {device_id} ] Payload: ", payload)
		
		# Get the variable to check, and convert to the correct value
		message_keys = list(payload.keys())
		if len(message_keys) != 1:
			add_log(
				database_connection,
				"Too many keys in the message",
				device_id
			)
			return

		key_to_check = message_keys[0]
		value = payload.get(key_to_check)
		try:
			source_correct_value = get_correct_value(key_to_check, value)
		except ValueError:
			add_log(
				database_connection,
				"Bad value format",
				device_id
			)
			return

		# Check the rules, checking if it has to be applied
		rules = get_rules(device_id, database_connection)
		for rule in rules:
			if self.debug:
				print(f"[ {device_id} ] Checking rule: ", rule['name'])
			# Convert the threshold to the correct value
			try:
				threshold = get_correct_value(key_to_check, rule['threshold'])
			except ValueError:
				add_log(
					database_connection,
					"Invalid threshold format",
				)
				return
			
			# Make the comparation, and check if it is correct
			try:
				comparation = compare_values(source_correct_value, threshold, rule['operator'])
			except ValueError:
				return
			
			if self.debug:
				print(f"[ {device_id} ] Comparation result: ", comparation)
			if not comparation:
				continue

			# Execute the command on the target device (send the command payload)
			target_device = rule['target_device_id']
			self.client.publish(
				f"redes/2312/10/{target_device}/command",
				rule['command_payload'],
				qos=1
			)

			# Notify django
			add_log(
				database_connection,
				f"Rule '{rule['name']}' applied",
				device_id
			)
			if self.debug:
				print(f"[ {device_id} ] Rule '{rule['name']}' applied")

		# Close the database connection
		database_connection.close()