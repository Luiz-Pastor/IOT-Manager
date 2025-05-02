from django.db import models
from .device import Device
from django.core.exceptions import ValidationError
import json

# If <SOURCE_DEVICE> <VALUE> <CONDITION> <THRESHOLD>,
# then send <COMMAND_PAYLOAD> to <TARGET_DEVICE>
class Rule(models.Model):
	"""
	Rule model to define the rules for the devices.
	"""

	class Operators(models.TextChoices):
		"""
		Operators for the rule conditions.
		"""
		GT = '>', 'Greater than'
		LT = '<', 'Less than'
		EQ = '==', 'Equal to'
		GTE = '>=', 'Greater than or equal to'
		LTE = '<=', 'Less than or equal to'

	# Name of the rule
	name = models.CharField(
		max_length=128,
		null=False, blank=False, unique=True
	)

	# Source device
	source_device = models.ForeignKey(
		Device,
		on_delete=models.CASCADE,
		related_name='rules_as_source',
	)

	# Operator to check
	operator = models.CharField(
		max_length=2,
		choices=Operators.choices,
	)

	# Condition value (to check)
	threshold = models.CharField(
		max_length=128,
	)

	# Target device
	target_device = models.ForeignKey(
		Device,
		on_delete=models.CASCADE,
		related_name='rules_as_target',
	)

	# Command payload to send
	command_payload = models.CharField(
		max_length=1024
	)

	# Created at and update dates
	created_at = models.DateTimeField(
		auto_now_add=True,
	)
	updated_at = models.DateTimeField(
		auto_now=True,
	)

	class Meta:
		ordering = ['name']
	
	def __str__(self):
		"""
		Returns a string representation of the rule.
		"""
		return self.name

	def clean(self):
		"""
		Validates the model fields.
		"""
		try:
			converted_payload = json.loads(self.command_payload)
		except json.decoder.JSONDecodeError:
			raise ValidationError("command_payload has to have a json format")

		if 'cmd' not in converted_payload:
			raise ValidationError("command_payload must contain 'cmd' key")
		super().clean()
	