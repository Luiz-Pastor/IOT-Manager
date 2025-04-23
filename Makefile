mosquitto:
	@docker run -it -p 1883:1883 eclipse-mosquitto

cache:
	@rm -rf $(shell find . -type d -name "__pycache__")

.PHONY: mosquitoo cache