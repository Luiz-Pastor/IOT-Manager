import requests

def get_devices_from_api(
	host: str,
	port: int
):
	"""
	Function to read the device data from the api and return it
	Args:
		host (str): Host of the Django server.
		port (int): Port of the Django server.
	"""	
	try:
		request = requests.get(
			f"http://localhost:8000/api/v1/devices/"
		)
		return request.json()
	except Exception:
		return None

def get_rules_from_api(
	host: str,
	port: int
):
	"""
	Function to read the rules data from the api and return it
	Args:
		host (str): Host of the Django server.
		port (int): Port of the Django server.
	"""	
	try:
		request = requests.get(
			f"http://localhost:8000/api/v1/rules/"
		)
		return request.json()
	except Exception:
		return None

def add_log_message(
	host: str,
	port:str,
	message: str,
	device_id: str = None
) -> None:
	"""
	Function to add a log message to the api

	Args:
		host (str): Host of the Django server.
		port (int): Port of the Django server.
		message (str): Message to be logged.
		device_id (str): ID of the device that generated
			the message. This argument can be None, so the
			log will not have a device associated.
	"""
	# Set the body to send
	body = { "message": message }
	if device_id:
		body["device"] = device_id

	try:
		request = requests.post(
			f"{host}:{port}/api/v1/logs/",
			data=body
		)
	except Exception:
		return None