import logging
import queue

from sawtooth_sdk.consensus.engine import Engine
from sawtooth_sdk.protobuf.validator_pb2 import Message

from consensus.consensus_message_pb2 import ConsensusMessage

LOGGER = logging.getLogger(__name__)


class CustomConsensusEngine(Engine):
    def __init__(self, path_config, component_endpoint):
        self._path_config = path_config
        self._component_endpoint = component_endpoint
        self._service = None

        # State Variable
        self._exit = False

    def name(self):
        return "custom-consensus"

    def version(self):
        return "0.1"

    def additional_protocols(self):
        return [('custom-consensus', '0.1')]

    def stop(self):
        self._exit = True

    def start(self, updates, service, startup_state):
        self._service = service
        LOGGER.info(msg="Custom Consensus Engine starting...")

        local_id = startup_state.local_peer_info.peer_id
        current_block_id = startup_state.chain_head.block_id
        settings = self._service.get_settings(current_block_id, ["sawtooth.consensus.custom_consensus.example"])

        LOGGER.info(msg="Local ID: {}".format(local_id))
        LOGGER.info(msg="Current Block ID: {}".format(current_block_id))
        LOGGER.info(msg="Example setting: {}".format(settings["sawtooth.consensus.custom_consensus.example"]))

        handlers = {
            Message.CONSENSUS_NOTIFY_BLOCK_NEW: self._handle_new_block,
            Message.CONSENSUS_NOTIFY_BLOCK_VALID: self._handle_valid_block,
            Message.CONSENSUS_NOTIFY_BLOCK_INVALID: self._handle_invalid_block,
            Message.CONSENSUS_NOTIFY_BLOCK_COMMIT: self._handle_committed_block,
            Message.CONSENSUS_NOTIFY_PEER_CONNECTED: self._handle_peer_connected,
            Message.CONSENSUS_NOTIFY_PEER_DISCONNECTED: self._handle_peer_disconnected,
            Message.CONSENSUS_NOTIFY_PEER_MESSAGE: self._handle_peer_msgs,
        }

        # Are we at the genesis block ?
        if startup_state.chain_head.previous_id == b'\x00\x00\x00\x00\x00\x00\x00\x00':
            LOGGER.info("Genesis block detected")
            # do something
        else:
            LOGGER.info("Non genesis block detected")
            # do something

        while True:
            try:
                try:
                    type_tag, data = updates.get(timeout=0.1)
                except queue.Empty:
                    pass
                else:
                    LOGGER.debug('Received message: %s',
                                 Message.MessageType.Name(type_tag))
                    try:
                        handle_message = handlers[type_tag]
                    except KeyError:
                        LOGGER.error('Unknown type tag: %s',
                                     Message.MessageType.Name(type_tag))
                    else:
                        handle_message(data)

                if self._exit:
                    break

            # pylint: disable=broad-except
            except Exception:
                LOGGER.exception("Unhandled exception in message loop")

    def _handle_new_block(self, block):
        LOGGER.info(msg="HANDLING NEW BLOCK")
        pass

    def _handle_valid_block(self, block_id):
        LOGGER.info(msg="HANDLING VALID BLOCK")
        pass

    def _handle_invalid_block(self, block_id):
        LOGGER.info(msg="HANDLING INVALID BLOCK")
        pass

    def _handle_committed_block(self, block_id):
        LOGGER.info(msg="HANDLING COMMITED BLOCK")
        pass

    def _handle_peer_msgs(self, msg):
        LOGGER.info(msg="HANDLING PEER MSG")
        consensus_msg = ConsensusMessage()
        consensus_msg.ParseFromString(msg[0].content)
        signer_id = msg[0].header.signer_id.hex()
        # do something

    def _handle_peer_connected(self, msg):
        LOGGER.info(msg="HANDLING PEER CONNECTED")
        pass

    def _handle_peer_disconnected(self, msg):
        LOGGER.info(msg="HANDLING PEER DISCONNECTED")
        pass

    # Wrapper around service.broadcast to be used for consensus related msgs
    def _broadcast(self, msg):
        self._service.broadcast(message_type=str(Message.CONSENSUS_NOTIFY_PEER_MESSAGE),
                                payload=msg.SerializeToString())

    # Wrapper around service.send_to to be used for consensus related msgs
    def _send_to(self, peer, msg):
        self._service.send_to(receiver_id=peer.encode('utf-8'), message_type=str(Message.CONSENSUS_NOTIFY_PEER_MESSAGE),
                              payload=msg.SerializeToString())
