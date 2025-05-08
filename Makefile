###############
# NOTE: Utils #
###############
cache:
	@rm -rf $(shell find . -type d -name "__pycache__")

controller:
	@python3 -m controller.controller --debug false

manager:
	@cd iot-manager; python3 manage.py runserver

####################
# NOTE: Containers #
####################

MOSQUITTO_NETWORK = mqtt-net

mqtt-network:
	@docker network inspect $(MOSQUITTO_NETWORK) >/dev/null 2>&1 || \
		docker network create $(MOSQUITTO_NETWORK)

mosquitto: mqtt-network
	@docker run -it --rm \
		--name mosquitto \
		--network $(MOSQUITTO_NETWORK) \
		-p 1883:1883 \
		-p 9001:9001 \
		-v ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf:ro \
		eclipse-mosquitto

mosquitto-web-ui: mqtt-network
	@docker run -it --rm \
		--name mosquitto-web-ui \
		--network $(MOSQUITTO_NETWORK) \
		-p 8000:80 \
		emqx/mqttx-web

.PHONY: cache controller manager mqtt-network mosquitto mosquitto-web-ui