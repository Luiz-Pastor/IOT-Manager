mosquitto:
	@docker run -it \
		-p 1883:1883 \
		-v ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf:ro \
		eclipse-mosquitto

cache:
	@rm -rf $(shell find . -type d -name "__pycache__")

.PHONY: mosquitto cache