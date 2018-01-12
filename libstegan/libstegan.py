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


import itertools
import math


def encode(conf_dict, message):
    """
    Converts the message to an image, according to the rules provided in conf_dict.
    Returns an image file.
    """
    if not _validate_ascii(message):
        raise Exception('Non-ASCII characters are disallowed!')


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
    # meaningful_channels_amount = list(conf_dict.values()).count(True)
    frequency = conf_dict['frequency']
    return len(message) + ((frequency - 1) * (len(message) - 1))

def _generate_dimensions(conf_dict, message):
    """
    Returns a 2-tuple consisting of width and height of an image which has
    no less than _minimal_pixel_count pixels.
    Only 1:1 ratio for now.
    """
    sq_side = math.ceil(math.sqrt(_minimal_pixel_count(conf_dict, message)))
    return (sq_side, sq_side)


class PixelIter:
    """
    An object to be iterated over.
    Returns 3-tuples which consist of a channel and x, y coordinates.
    Currently supports only 1:1 image ratio.
    """

    def __init__(self, conf_dict, message):
        self.conf_dict = conf_dict
        dim = _generate_dimensions(conf_dict, message)
        self.width = dim[0]
        self.height = dim[1]
        # let's assume that the red, green and blue are the only bools there
        meaningful_channels = [
            col for col in conf_dict.keys() if conf_dict[col] == True
        ]
        self.col_cycle = itertools.cycle(meaningful_channels)
        self.current_index = 0
        self.divisor = conf_dict['frequency']

    def __iter__(self):
        return self

    def __next__(self):
        ind = self.current_index
        self.current_index += 1
        if ind >= self.width * self.height:
            raise StopIteration
        row = ind / self.divisor
        column = ind % self.divisor
        if not ind % self.divisor:
            return (next(self.col_cycle), row, column)
        return ('whatever', row, column)
