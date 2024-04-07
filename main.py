"""Encoder for glebi's PewPewLive screen"""

import signal
import json
import sys
import os

from loguru import logger


def sigint_handler(sig, frame):
    """Handle SIGINT signal (e.g. Ctrl+C)"""
    logger.error("Got SIGINT, stopping...")

    sys.exit(0)


def setup(config_path: str) -> None:
    """Setup logging, get config, etc"""
    global logger, db_con, db_cur

    logger.remove(0)
    logger = logger.opt(colors=True)

    logger.add(sys.stderr, level="TRACE")

    with open(config_path, "r", encoding="UTF-8") as file:
        config = json.load(file)
        logger.debug("Loaded config from <m>{}</>", config_path)

    logs_path = config["logs_path"]
    if logs_path is not None:
        if not os.path.exists(logs_path):
            logger.warning("Logs folder does not exist, creating... ({})",
                           logs_path)
            os.makedirs(logs_path)

        logger.add(os.path.join(
            logs_path, "log-{time}.log"), rotation="00:00", level="TRACE")

    logger.debug("Registering signal handler for <y>{}</>",
                 "signal.SIGINT")
    signal.signal(signal.SIGINT, sigint_handler)

    return config


def main(config_file: str = "config.json") -> None:
    """Start the encoder"""
    global client, config
    logger.info("Starting the encoder... (config_file=<m>{}</>)", config_file)

    config = setup(config_file)

    logger.info("Job done, exiting...")


if __name__ == "__main__":
    logger.info('__name__ == "__main__", starting the program...')
    main()
