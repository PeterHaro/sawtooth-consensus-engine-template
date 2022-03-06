SHELL := /bin/bash

protobuf:
	protoc -I=sawtooth_dpos/protos --python_out=sawtooth_dpos/consensus sawtooth_dpos/protos/*.proto

run:
	docker-compose up -d --build