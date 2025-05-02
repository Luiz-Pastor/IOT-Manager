from django.db import models

class Device(models.Model):
	# Device id
	id = models.CharField(
		max_length=128,
		primary_key=True
	)

	# Server host
	host = models.CharField(
		max_length=128,
		default='redes2.ii.uam.es',
	)

	# Server port
	port = models.PositiveIntegerField(
		default=1883,
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
		return f"redes/2312/10/{self.id}/status"
	
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
