from django.db import models
from .device import Device
from django.core.exceptions import ValidationError

class DummySensor(Device):
	# Interval
	interval = models.FloatField(
		default=1.0,
	)

	# Min value
	min_value = models.FloatField(
		default=20.0,
	)

	# Max value
	max_value = models.FloatField(
		default=30.0,
	)

	# Increment
	increment = models.FloatField(
		default=1.0,
	)

	def clean(self):
		"""
		Validates the model fields.
		"""
		if self.min_value > self.max_value:
			raise ValidationError("min_value must be less than max_value")
		if self.increment <= 0:
			raise ValidationError("increment must be greater than 0")
		if self.interval <= 0:
			raise ValidationError("interval must be greater than 0")
		super().clean()
	
	def __str__(self):
		"""
		Returns a string representation of the device.
		"""
		return "DummySensor " + super().__str__()
	
	@property
	def variable_name(self) -> str:
		"""
		Returns the variable name of the device message key.
		"""
		return "temperature"