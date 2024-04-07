"""Module for transforming given image"""

import sys

from PIL import Image
from loguru import logger

logger = logger.opt(colors=True)


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
