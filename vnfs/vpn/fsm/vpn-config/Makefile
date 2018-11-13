TARGET_DIR=/vpn-config
SOURCE_DIR=vpn_css

all: run

dev:
	docker run -it --rm=true --link 'broker:broker' --env 'SON_EMULATOR=1' -v "$$(pwd)/test/:$(TARGET_DIR)/test/" -v "$$(pwd)/$(SOURCE_DIR)/:$(TARGET_DIR)/$(SOURCE_DIR)/" -v "$$(pwd)/ansible:$(TARGET_DIR)/ansible/"  -v '/var/run/docker.sock:/var/run/docker.sock' sonata-psa/dev-fsm-vpn /bin/bash

run:
	docker run -it --rm=true --link 'broker:broker' --env 'SON_EMULATOR=1' -v "$$(pwd)/test/:$(TARGET_DIR)/test/" -v "$$(pwd)/$(SOURCE_DIR)/:$(TARGET_DIR)/$(SOURCE_DIR)/" -v '/var/run/docker.sock:/var/run/docker.sock' sonata-psa/dev-fsm-vpn python test/test_configuration.py

build:
	docker build -t sonata-psa/dev-fsm-vpn .

broker:
	docker run -d --name broker rabbitmq:3-management
