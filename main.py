"""Encoder for glebi's PewPewLive screen"""

import signal
import json
import sys
import os

from PIL import Image

from loguru import logger

DEFAULT_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


def sigint_handler(sig, frame):
    """Handle SIGINT signal (e.g. Ctrl+C)"""
    logger.error("Got SIGINT, stopping...")

    sys.exit(0)


def load_config(config_path: str) -> dict:
    """Load config from given path, use cli arguments too"""
    logger.debug("Loading config, config_path: <m>{}</>", config_path)

    if config_path is None:
        config = {}
    else:
        try:
            with open(config_path, "r", encoding="UTF-8") as file:
                config = json.load(file)
                logger.debug("Loaded config from <m>{}</>", config_path)
        except FileNotFoundError:
            config = {}

    if config == {}:
        logger.warning("Failed to load config, using arguments for image_path")
        if len(sys.argv) > 1:
            image_path = sys.argv[1]
        else:
            logger.error("Image not specified")
            sys.exit(1)
        config.update({"input_path": image_path})

    return config


def setup(config_path: str) -> None:
    """Setup logging, get config, etc"""
    global logger, db_con, db_cur

    logger.remove(0)
    logger = logger.opt(colors=True)

    logger.add(sys.stderr, level="TRACE")

    config = load_config(config_path)

    logs_path = config.get("logs_path")
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
    logger.debug("Loading image, in config image_path: <m>{}</>", image_path)

    # [TODO: prioritize argument image]
    if image_path is None:
        if len(sys.argv) > 1:
            image_path = sys.argv[1]
        else:
            logger.error("Image not specified")
            sys.exit(1)

    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        logger.error("Specified image file not found")
        sys.exit(1)

    return image


def to_bilevel(image: Image, sets: dict) -> Image:
    """Convert image to black and white"""
    logger.debug("Converting image to black and white, settings: <w>{}</>",
                 sets)
    # image = image.convert("L")  # convert image to greyscale
    image = image.convert("1", dither=Image.Dither.FLOYDSTEINBERG)

    return image


def get_size(size_factor: int) -> tuple[int, int]:
    """Get size from size factor, using the formula"""
    logger.debug("Getting size, size_factor: <m>{}</>", size_factor)

    width = size_factor * 14
    height = 1200 // size_factor
    logger.trace("Got size: <w>{}</>", (width, height))

    return width, height


def resize_image(image: Image, size_factor: int, sets: dict) -> Image:
    """Resize image"""
    logger.debug(
        "Resizing image, size_factor: <m>{}</>, settings: <w>{}</>",
        size_factor, sets
    )

    size = get_size(size_factor)
    default_mode = "resize"
    if sets is not None:
        mode = sets.get("mode", default_mode)
    else:
        mode = default_mode

    if mode == "crop":
        image = image.crop((0, 0, size[0], size[1]))
    elif mode == "resize":
        image = image.resize(size)
    # [TODO: implement]
    #  elif mode == "reduce":
    #      image = image.reduce(size)
    else:
        logger.error("Got unknown resize mode: <m>{}</>", mode)
        sys.exit(1)

    return image


# [TODO: support different set size (not just 3)]
def encode_36(num: int, sets: dict) -> str:
    """Encode number with 36byte system, custom alphabet"""
    # logger.trace("Encoding number, num: <m>{}</>, settings: <w>{}</>",
    #              num, sets)

    alphabet = sets.get("alphabet", DEFAULT_ALPHABET)
    s = len(alphabet)

    # thanks, glebi, i stole this :з
    result1 = alphabet[num // (s ** 2)]
    result2 = alphabet[(num // s) % s]
    result3 = alphabet[num % s]

    return result1 + result2 + result3


def encode_image(size_factor: int, image: Image, sets: dict) -> Image:
    """Encode image"""
    logger.debug("Encoding image, size_factor: <m>{}</>, settings: <w>{}</>",
                 size_factor, sets)

    encoded_size = encode_36(size_factor, sets)

    # [TODO: fix some awful code]
    image_bytes = [str(bin(x))[2:].ljust(8, "0") for x in image.tobytes()]

    individual_bytes = []
    for x in image_bytes:
        individual_bytes += x

    encoded = encoded_size
    for i in range(len(individual_bytes)//14):
        encoded += encode_36(int("".join(individual_bytes[:14]), base=2), sets)
        individual_bytes = individual_bytes[14:]
        # logger.trace("Encoded bytes: <m>{}</>", encoded)

    # image.save("results.png")

    return 'return"' + encoded + '"'


def main(config_file: str = "config.json") -> None:
    """Start the encoder"""
    global client, config
    logger.info("Starting the encoder... (config_file=<m>{}</>)", config_file)

    config = setup(config_file)
    size_factor = config.get("size_factor", 10)
    conv_sets = get_conv_sets(config)
    encoding_sets = config.get("encoding", {})

    image = load_image(config.get("input_path"))
    image = to_bilevel(image, conv_sets["to_bilevel"])
    image = resize_image(image, size_factor, conv_sets["resize"])

    result = encode_image(size_factor, image, encoding_sets)
    # logger.opt(colors=False).success(result)
    with open("results.lua", "w", encoding="UTF-8") as file:
        file.write(result)

    logger.info("Job done, exiting...")


if __name__ == "__main__":
    logger.info('__name__ == "__main__", starting the program...')
    main()
