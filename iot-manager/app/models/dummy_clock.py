from django.db import models
from .device import Device
from datetime import datetime
from django.core.exceptions import ValidationError

class DummyClock(Device):
	# Start time
	start_time = models.TimeField(
		default=datetime.now().time()
	)

	# Increment
	increment = models.PositiveIntegerField(
		default=1,
	)

	# Rate
	rate = models.FloatField(
		default=1.0,
	)

	def clean(self):
		"""
		Validates the model fields.
		"""
		if self.increment <= 0:
			raise ValidationError("increment must be greater than 0")
		if self.rate <= 0:
			raise ValidationError("rate must be greater than 0")
		super().clean()
	
	def __str__(self):
		"""
		Returns a string representation of the device.
		"""
		return "DummyClock " + super().__str__()
	
	@property
	def variable_name(self) -> str:
		"""
		Returns the variable name of the device message key.
		"""
		return "time"