from typing import Dict, List

class Device:
	def __init__(
		self,
		id: str,
		host: str,
		port: int,
		device_type: str,
		configuration: Dict[str, str]
	):
		"""
		Constructor of the Device class.
		Args:
			id (str): ID (name) of the device
			host (str): Host of the device.
			port (int): Port of the device.
			device_type (str): Type of the device.
			configuration (Dict[str, str]): Configuration of the device.
		"""
		self.id = id
		self.host = host
		self.port = port
		self.type = device_type
		self.configuration = configuration
	
	def __str__(self):
		return f"{self.type}({self.id}, {self.host}, {self.port})"
	
	def __repr__(self):
		return f"{self.type}({self.id}, {self.host}, {self.port})"

	@classmethod
	def from_api(cls, data: List[Dict[str, str]]) -> List['Device']:
		"""
		Method to create all the devices got from the API
		"""
		devices = []
		for current in data:
			try:
				new_device = cls(
					current['id'],
					current['host'],
					current['port'],
					current['device_type'],
					current['configuration']
				)
				devices.append(new_device)
			except Exception:
				return None

		return devices