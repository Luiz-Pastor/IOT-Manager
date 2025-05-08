from app.models import DummySwitch, DummySensor
from django.test import TestCase
from paho.mqtt.client import Client
import time
import json

class TestDevice(TestCase):
	"""
	"""
	def setUp(self):
		self.message_count = 0
		self.client: Client = Client()
		self.client.on_message = self.on_message

	def on_message(self, client, userdata, message):
		self.message_count += 1

	def test_switch_01(self):
		"""
		"""
		# Connect with broker (mosquitto)
		try:
			self.client.connect("localhost", 1883)
			self.client.loop_start()
		except Exception as e:
			self.fail(f"Failed to connect to broker: {e}")

		# Create the switch, execute it and change
		switch = DummySwitch(
			id="switch-test-01",
			host="localhost",
			port=1883,
			probability=0
		)
		switch_pid = switch.start_process(['--probability', '0', '--debug', 'true'])
		self.assertNotEquals(switch_pid, None)
		self.message_count = 0

		# Subscribe to the switch topic and send the message
		self.client.subscribe("redes/2312/10/switch-test-01/state")
		self.client.publish(
			"switch-test-01/command",
			json.dumps({
				"command": "set",
				"state": "ON"
			}),
		)

		# Wait for the message to be received
		time.sleep(2)

		# Stop the client loop
		self.client.loop_stop()
		switch.stop_process()

		# Assert that the message was received
		self.assertGreater(self.message_count, 0)

	def test_sensor_02(self):
		"""
		"""
		# Connect with broker (mosquitto)
		try:
			self.client.connect("localhost", 1883)
			self.client.loop_start()
		except Exception as e:
			self.fail(f"Failed to connect to broker: {e}")

		# Create the switch, execute it and change
		sensor = DummySensor(
			id="sensor-test-02",
			host="localhost",
			port=1883,
			interval=1,
			min_value=0,
			max_value=10,
			increment=1
		)
		switch_pid = sensor.start_process([
			'--interval', '1',
			'--min', '0', '--max', '10',
			'--increment', '1'
		])
		self.assertNotEquals(switch_pid, None)
		self.message_count = 0

		# Subscribe to the switch topic and send the message
		self.client.subscribe("redes/2312/10/sensor-test-02/state")

		# Wait for the message to be received
		time.sleep(5)

		# Stop the client loop
		self.client.loop_stop()
		sensor.stop_process()

		# Assert that the message was received
		self.assertGreater(self.message_count, 3)
		