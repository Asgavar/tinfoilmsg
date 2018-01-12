"""
A small helper library for tinfoilmsg which handles the image and text
transformations.
The dictionary which is supposed to be passed to these functions and classes
can look like this:
{
    'red': True,
    'green': False,
    'blue': True,
    'frequency': 3
}
This will tell them that only red and blue channels are interesting, and pixels
on positions dividable by 3 in particular.
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


def _minimal_pixel_count(conf_dict, message):
    """
    Calculates the minimal amount of pixels needed to encode the message.
    """
    # let's assume that the red, green and blue are the only bools there
    meaningful_channels_amount = list(conf_dict.values()).count(True)
    frequency = conf_dict['frequency']
    return len(message) + ((frequency - 1) * (len(message) - 1))


class RGBCycler:
    def __init__(conf_dict):
        pass
