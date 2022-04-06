SHELL := /bin/bash

protobuf:
	protoc -I=src/protos --python_out=src/consensus src/protos/*.proto

run:
	docker-compose up -d --build