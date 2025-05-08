from django.db import models
from .device import Device
from django.core.exceptions import ValidationError

class DummySwitch(Device):
	# Probability
	probability = models.FloatField(
		default=0.3
	)

	def clean(self):
		"""
		Validates the model fields.
		"""
		if self.probability < 0.0 or self.probability > 1.0:
			raise ValidationError("probability must be between 0 and 1")
		super().clean()

	def __str__(self):
		"""
		Returns a string representation of the device.
		"""
		return "DummySwitch " + super().__str__()

	@property
	def variable_name(self) -> str:
		"""
		Returns the variable name of the device message key.
		"""
		return "state"
	
	@property
	def device_type(self) -> str:
		"""
		Returns the device type.
		"""
		return "dummy-switch"