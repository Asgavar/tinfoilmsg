"""
A small helper library for tinfoilmsg which handles the image and text
transformations.
"""


def encode():
    pass  # TODO


def decode():
    pass  # TODO


def _validate_ascii(message):
    """
    Ensure that the message provided is composed of ASCII letters only,
    it's crucial since it will be mapped to RGB values which can't exceed 255.
    """
    return all(ord(c) < 128 for c in message)


class RGBCycler:
    def __init__(conf_dict):
        pass
