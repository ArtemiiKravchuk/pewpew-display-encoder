"""Encoder for glebi's PewPewLive screen"""

import signal
import json
import sys
import os

from PIL import Image

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


def get_conv_sets(config: dict) -> dict:
    """Get conversion settings"""
    logger.debug("Getting conversion settings")
    conv_sets = config.get("conversion_settings")
    if conv_sets is not None:
        to_bilevel = conv_sets.get("to_bilevel")
        resize = conv_sets.get("resize")
    else:
        to_bilevel = None
        resize = None

    results = {
        "to_bilevel": to_bilevel,
        "resize": resize
    }
    logger.trace("Got conversion settings: <w>{}</>", results)
    return results


def load_image(image_path: str) -> Image:
    """Load image from disk"""
    logger.debug("Loading image from <m>{}</>", image_path)
    image = Image.open(image_path)

    return image


def convert_black_and_white(image: Image, sets: dict) -> Image:
    """Convert image to black and white"""
    logger.debug("Converting image to black and white")
    # image = image.convert("L")  # convert image to greyscale
    image = image.convert("1")

    return image


def resize_image(image: Image, sets: dict) -> Image:
    """Resize image"""
    logger.debug("Resizing image to <m>{}</>", (140, 120))
    image = image.resize((140, 120))

    return image


def main(config_file: str = "config.json") -> None:
    """Start the encoder"""
    global client, config
    logger.info("Starting the encoder... (config_file=<m>{}</>)", config_file)

    config = setup(config_file)
    conv_sets = get_conv_sets(config)

    image = load_image(config["input_path"])
    image = convert_black_and_white(image, conv_sets["to_bilevel"])
    image = resize_image(image, conv_sets["resize"])

    image.save('result.png')

    logger.info("Job done, exiting...")


if __name__ == "__main__":
    logger.info('__name__ == "__main__", starting the program...')
    main()
