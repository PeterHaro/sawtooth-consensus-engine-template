# Template - Sawtooth Consensus Engine

This project is a template to develop a new consensus engine for [Hyperledger Sawtooth](https://github.com/hyperledger/sawtooth-core) based on the [Python SDK](https://github.com/hyperledger/sawtooth-sdk-python).
 
## Getting started

Running `make run` will spin off 11 consensus nodes using docker-compose. 

The logs of an untouched custom consensus engine should look like those:

```
[2022-03-06 20:14:09.927 INFO     main] Starting Custom Consensus Engine Driver
[2022-03-06 20:14:09.930 DEBUG    selector_events] Using selector: ZMQSelector
[2022-03-06 20:14:09.985 INFO     zmq_driver] Received activation message with startup state: StartupInfo(...)
[2022-03-06 20:14:09.988 INFO     custom_engine] Custom Consensus Engine starting...
[2022-03-06 20:14:10.004 INFO     custom_engine] Local ID: b'...'
[2022-03-06 20:14:10.005 INFO     custom_engine] Current Block ID: b'...'
[2022-03-06 20:14:10.005 INFO     custom_engine] Example setting: example_value
[2022-03-06 20:14:10.006 INFO     custom_engine] Genesis block detected
```

## Protobuf

You can generate the protobuf by running `make protobuf`, given that `protoc` is installed.