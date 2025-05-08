from app.models import DummySwitch, DummySensor, Rule
from django.test import TransactionTestCase
from paho.mqtt.client import Client
import time
import json
import os
import subprocess
import signal
from django.db import connection

class TestController(TransactionTestCase):
	"""
	"""
	def setUp(self):
		self.client: Client = Client()
		self.switch_ok = True

	def no_message(self, client, userdata, message):
		pass

	def check_switch(self, client, userdata, message):
		message_payload = json.loads(message.payload.decode('utf-8'))
		if message_payload.get("state") == "ON":
			self.switch_ok = True

	def test_constroller_01(self):
		"""
		"""
		# Connect with broker (mosquitto)
		self.client.on_message = self.no_message
		try:
			self.client.connect("localhost", 1883)
			self.client.loop_start()
		except Exception as e:
			self.fail(f"Failed to connect to broker: {e}")

		# Execute the controller
		cmd = [
			"python3", '-m', 'controller.controller',
			"--host", "localhost", '--database', 'test-db.sqlite3'
		]
		env = os.environ.copy()
		env['PYTHONPATH'] = '../'
		process = subprocess.Popen(
			cmd,
			env=env,
		)
		controller_pid = process.pid
		time.sleep(1)

		# Create the sensor, switch and rule
		switch = DummySwitch.objects.create(
			id="swtc01",
			host="localhost",
			port=1883,
			probability=0
		)
		sensor = DummySensor.objects.create(
			id="sstc01",
			host="localhost",
			port=1883,
			min_value=10,
			max_value=12,
			interval=1,
			increment=1
		)
		rule1 = Rule.objects.create(
			name="Test 10",
			source_device=sensor,
			operator="==",
			threshold=10,
			target_device=switch,
			command_payload='{"cmd":"set","state":"ON"}'
		)
		rule2 = Rule.objects.create(
			name="Test 11",
			source_device=sensor,
			operator="==",
			threshold=11,
			target_device=switch,
			command_payload='{"cmd":"set","state":"ON"}'
		)
		connection.commit()

		# Execute the devices
		switch_pid = switch.start_process(['--probability', '0']) # Start => OFF, por lo que deberia cambiar
		sensor_pid = sensor.start_process(['--min', '10', '--max', '11', '--interval', '1', '--increment', '1'])
		self.assertNotEquals(switch_pid, None)
		self.assertNotEquals(sensor_pid, None)

		# Wait until the rule is executed (min one time)
		time.sleep(2)

		# Check the switch state
		self.client.subscribe("redes/2312/10/sstc01/state")
		self.client.on_message = self.check_switch
		self.client.publish(
			"redes/2312/10/swtc01/command",
			json.dumps({
				"cmd": "get"
			}),
		)
		time.sleep(1)

		# Stop the client loop
		self.client.loop_stop()
		switch_stop = switch.stop_process()
		sensor_stop = sensor.stop_process()
		self.assertTrue(switch_stop)
		self.assertTrue(sensor_stop)

		try:
			os.kill(controller_pid, signal.SIGKILL)
		except:
			pass

		# Check if the status changed
		self.assertTrue(self.switch_ok)
