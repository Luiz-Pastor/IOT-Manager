from django.db import models

class Log(models.Model):
	"""
	Class to save the devices logs
	"""
	# Date when the log was done
	timestamp = models.DateTimeField(
		auto_now_add=True
	)

	# Device name
	device = models.CharField(
		max_length=128,
		null=False, blank=False
	)

	# Log message
	message = models.TextField(
		null=False, blank=False
	)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.message}"
