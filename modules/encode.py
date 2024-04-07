"""Module for encoding given image"""

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
