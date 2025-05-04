from typing import List, Dict

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

	def __str__(self):
		return f"Rule({self.name}, {self.source_device_id}, {self.operator}, {self.threshold})"

	def __repr__(self):
		return f"Rule({self.name}, {self.source_device_id}, {self.operator}, {self.threshold})"

	@classmethod
	def from_api(cls, data: List[Dict[str, str]]) -> List['Rule']:
		"""
		Method to create all the rules got from the API
		"""
		rules = []
		for current in data:
			try:
				new_rule = cls(
					current['id'],
					current['name'],
					current['source_device'],
					current['operator'],
					current['threshold'],
					current['target_device'],
					current['command_payload']
				)
				rules.append(new_rule)
			except Exception:
				return None

		return rules