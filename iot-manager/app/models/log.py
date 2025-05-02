from django.db import models

class Log(models.Model):
	"""
	Class to save the devices logs
	"""
	# Log message
	message = models.TextField()

	# Date when the log was done
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['timestamp']

	def __str__(self):
		return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.message}"
