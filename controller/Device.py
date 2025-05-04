from typing import Dict, List

class Device:
	def __init__(
		self,
		host: str,
		port: int,
		device_type: str,
		configuration: Dict[str, str]
	):
		"""
		Constructor of the Device class.
		Args:
			host (str): Host of the device.
			port (int): Port of the device.
			device_type (str): Type of the device.
			configuration (Dict[str, str]): Configuration of the device.
		"""
		self.host = host
		self.port = port
		self.type = device_type
		self.configuration = configuration
	