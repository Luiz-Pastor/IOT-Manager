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
