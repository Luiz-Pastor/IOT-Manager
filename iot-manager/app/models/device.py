from django.db import models
import subprocess
import os
import signal

class Device(models.Model):
	# Device id
	id = models.CharField(
		max_length=128,
		primary_key=True
	)

	# Server host
	host = models.CharField(
		max_length=128,
		default='localhost',
	)

	# Server port
	port = models.PositiveIntegerField(
		default=1883,
	)

	# Device PID
	pid = models.IntegerField(
		null=True,
		blank=True,
		editable=False
	)

	class Meta:
		ordering = ['id']
	
	def __str__(self):
		"""
		Returns a string representation of the device.
		"""
		return f"{self.id} @ {self.host}:{self.port}"

	def get_concrete(self):
		for rel in self._meta.related_objects:
			if rel.one_to_one and rel.auto_created:
				accessor = rel.get_accessor_name()
				try:
					return getattr(self, accessor)
				except models.ObjectDoesNotExist:
					continue
		return self

	###############
	# NOTE: Topic #
	###############
	@property
	def status_topic(self) -> str:
		"""
		Returns the status topic of the device.
		"""
		return f"redes/2312/10/{self.id}/state"
	
	@property
	def command_topic(self) -> str:
		"""
		Returns the command topic of the device.
		"""
		return f"redes/2312/10/{self.id}/command"

	###################################
	# NOTE: Key on the message status #
	###################################
	@property
	def variable_name(self) -> str:
		"""
		Returns the variable name of the device message key.
		"""
		concrete = self.get_concrete()
		if concrete is self:
			raise NotImplementedError("Subclasses must implement this method")

		try:
			return concrete.variable_name
		except AttributeError:
			raise NotImplementedError("Subclasses must implement this method")


	############################
	# NOTE: Process management #
	############################

	@property
	def device_type(self) -> str:
		"""
		Returns the type of device.
		"""
		if hasattr(self, 'dummysensor'):
			return 'dummy-sensor'
		if hasattr(self, 'dummyclock'):
			return 'dummy-clock'
		if hasattr(self, 'dummyswitch'):
			return 'dummy-switch'

	def start_process(self, extra_args: list = None):
		"""
		Starts the device process.
		Args:
			extra_args (list): Extra arguments to pass to the process.
		"""
		if self.pid is not None:
			return

		scripts_path = {
			'dummy-sensor': 'iot.dummy-sensor',
			'dummy-clock': 'iot.dummy-clock',
			'dummy-switch': 'iot.dummy-switch',
		}

		module = scripts_path.get(self.device_type)
		cmd = [
			'python3', '-m', module,
			'--host', self.host, '--port', str(self.port),
			self.id
		]
		if extra_args:
			cmd.extend(extra_args)
		
		env = os.environ.copy()
		env['PYTHONPATH'] = '../'

		# Start
		process = subprocess.Popen(cmd, env=env)
		self.pid = process.pid
		self.save(update_fields=['pid'])

	def stop_process(self) -> None:
		"""
		Stops the device process.
		"""
		if self.pid is None:
			return

		try:
			os.kill(self.pid, signal.SIGTERM)
		except OSError:
			pass
		self.pid = None
		self.save(update_fields=['pid'])