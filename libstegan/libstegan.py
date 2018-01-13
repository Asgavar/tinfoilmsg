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
import random

from PIL import Image


def encode(conf_dict, message):
    """
    Converts the message to an image, according to the rules provided in conf_dict.
    Returns an image file.
    """
    if not _validate_ascii(message):
        raise Exception('Non-ASCII characters are disallowed!')
    dimensions = _generate_dimensions(conf_dict, message)
    img = Image.new('RGB', dimensions)
    img_pixels = img.load()
    msg_pointer = 0
    for pixel in PixelIter(conf_dict, message):
        new_rgb_tuple = _craft_pixel(pixel[0], message, msg_pointer)
        img_pixels[pixel[1], pixel[2]] = new_rgb_tuple
        if pixel[0] in ('red', 'green', 'blue'):
            msg_pointer += 1
    return img


def decode(conf_dict, image):
    """
    Extracts the message hidden in the image, according to the rules from conf_dict.
    Returns the message string.
    """
    # FIXME
    msg_prosthesis = 'a'*(image.size[0]*image.size[1]//conf_dict['frequency'])
    msg_str = ''
    colors = ['red', 'green', 'blue']
    img_pixels = image.load()
    for pixel_info in PixelIter(conf_dict, msg_prosthesis):
        if pixel_info[0] == 'whatever':
            continue
        xy = (pixel_info[1], pixel_info[2])
        which_color = colors.index(pixel_info[0])
        letter_ord = img_pixels[xy][which_color]
        msg_str += chr(letter_ord)
    return msg_str


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


def _random_color():
    """
    Does exactly what it is supposed to do.
    """
    return random.randint(0, 255)


def _craft_pixel(color, message, msg_pointer):
    """
    Returns a RGB tuple inside which there is or there is not a letter.
    """
    if color in ('red', 'green', 'blue'):
        letter = ord(message[msg_pointer])
    if color == 'whatever':
        return (_random_color(), _random_color(), _random_color())
    if color == 'red':
        return (letter, _random_color(), _random_color())
    if color == 'green':
        return (_random_color(), letter, _random_color())
    if color == 'blue':
        return (_random_color(), _random_color(), letter)


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
        # let's assume that red, green and blue are the only bools there
        meaningful_channels = [
            col for col in conf_dict.keys() if conf_dict[col] is True
        ]
        self.col_cycle = itertools.cycle(meaningful_channels)
        self.current_index = 0
        self.divisor = conf_dict['frequency']
        self.msg_threshold = len(message) * 3

    def __iter__(self):
        return self

    def __next__(self):
        ind = self.current_index
        self.current_index += 1
        if ind >= self.width * self.height:
            raise StopIteration
        row = ind // self.width
        column = ind % self.width
        if not ind % self.divisor and self.current_index < self.msg_threshold:
            return (next(self.col_cycle), column, row)
        return ('whatever', column, row)
