"""Module for encoding given image"""

import sys

from PIL import Image
from loguru import logger

logger = logger.opt(colors=True)

DEFAULT_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


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

    pixels = [int(x) for x in image.getdata()]
    for i, pixel in enumerate(pixels):
        pixels[i] = "0" if pixel == 0 else "1"
    # print(pixels)

    encoded = encoded_size
    for i in range(len(pixels)//14):
        encoded += encode_36(int("".join(pixels[:14]), base=2), sets)
        # print("Encoding: {}".format(int("".join(pixels[:14]), base=2), sets))
        pixels = pixels[14:]
        # logger.trace("Encoded bytes: <m>{}</>", encoded)

    # image.save("results.png")

    return 'return"' + encoded + '"'
