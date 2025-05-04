class Rule:
	def __init__(
		self,
		id,
		name,
		source_device_id,
		operator,
		threshold,
		target_device_id,
		command_payload
	):
		self.id = id
		self.name = name
		self.source_device_id = source_device_id
		self.operator = operator
		self.threshold = threshold
		self.target_device_id = target_device_id
		self.command_payload = command_payload
