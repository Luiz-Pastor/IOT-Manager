import sqlite3
from datetime import datetime

def check_database(database: str) -> bool:
	"""
	Check if the database exists.
	Args:
		database (str): The path to the database.
	Returns:
		bool: True if the database exists, False otherwise.
	"""
	try:
		with open(database, 'r') as f:
			return True
	except FileNotFoundError:
		return False

def create_connection(database: str) -> sqlite3.Connection:
	"""
	Function to create a connection to the database
	Args:
		database (str): Path to the database file.
	Returns:
		sqlite3.Connection: Connection object to the database.
	"""
	# Connect with the database
	connection = sqlite3.connect(database)

	# Change the format of the queries
	connection.row_factory = sqlite3.Row

	# Activate WAL and NORMAL mode
	connection.execute("PRAGMA journal_mode=WAL;")
	connection.execute("PRAGMA synchronous=NORMAL;")

	# Return the connection
	return connection

def get_rules(source_device: str, database: sqlite3.Connection) -> list:
	"""
	Get the rules from the database.
	Args:
		source_device (str): The source device id.
		database (sqlite3.Connection): The connection to the database.
	Returns:
		list: The list of rules.
	"""
	cursor = database.cursor()
	cursor.execute(
		"SELECT * FROM app_rule WHERE source_device_id = ?",
		(source_device,)
	)
	rules = cursor.fetchall()
	return rules

def add_log(database: sqlite3.Connection, message: str, device_id: str = None) -> None:
	"""
	Add a log to the database.
	Args:
		database (sqlite3.Connection): The connection to the database.
		message (str): The message to log.
		device_id (str): The device id that generated the log.
	"""
	cursor = database.cursor()
	cursor.execute(
		"INSERT INTO app_log (message, device, timestamp) VALUES (?, ?, ?)",
		(message, device_id, datetime.now(),)
	)
	database.commit()
