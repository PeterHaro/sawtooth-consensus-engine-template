import argparse
import logging
import sys

import pkg_resources

from sawtooth_sdk.consensus.zmq_driver import ZmqDriver
from sawtooth_sdk.processor.exceptions import LocalConfigurationError
from sawtooth_sdk.processor.log import log_configuration
from sawtooth_sdk.processor.log import init_console_logging
from sawtooth_sdk.processor.config import get_log_dir

from config.path import load_path_config
from engine.custom_engine import CustomConsensusEngine

DISTRIBUTION_NAME = "sawtooth-custom-consensus-engine"

LOGGER = logging.getLogger(__name__)


def parse_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-C', '--connect',
        default='tcp://localhost:5050',
        help='Endpoint for the validator connection')

    parser.add_argument(
        '--component',
        default='tcp://localhost:4004',
        help='Endpoint for the validator component connection')

    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='Increase output sent to stderr')

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='print version information')

    return parser.parse_args(args)


def main(args=None):
    try:
        path_config = load_path_config()
    except LocalConfigurationError as local_config_err:
        LOGGER.error(str(local_config_err))
        sys.exit(1)

    if args is None:
        args = sys.argv[1:]
    opts = parse_args(args)

    try:
        log_dir = get_log_dir()
        log_configuration(
            log_dir=log_dir,
            name='custom-consensus-engine')

        init_console_logging(verbose_level=opts.verbose)

        driver = ZmqDriver(
            CustomConsensusEngine(
                path_config=path_config,
                component_endpoint=opts.component,
               ))

        LOGGER.info(msg="Starting Custom Consensus Engine Driver")
        driver.start(endpoint=opts.connect)
        LOGGER.info(msg="Custom Consensus Engine Driver started")
    except KeyboardInterrupt:
        pass
    except Exception:  # pylint: disable=broad-except
        LOGGER.exception("Error starting Custom Consensus Engine")
    finally:
        pass


if __name__ == "__main__":
    main()
