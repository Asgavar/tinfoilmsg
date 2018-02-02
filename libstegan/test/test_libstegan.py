import libstegan


generic_conf_dict =  {
    'red': True,
    'green': False,
    'blue': True,
    'frequency': 3
}
generic_msg = 'abcde'
generic_img = libstegan.encode(generic_conf_dict, generic_msg)


def test_imported_correctly():
    assert 'PixelIter' in libstegan.__dict__

def test_ascii_validation_true():
    msg = 'An ascii-only string :) ;>'
    assert libstegan._validate_ascii(msg) == True

def test_ascii_validation_false():
    msg = 'Żażółć gęślą żółtą jaźń'
    assert libstegan._validate_ascii(msg) == False

def test_minimal_pixel_count_for_msg_len_5_and_freq_3():
    # I've done it by hand on a sheet of paper so I hope that's correct
    assert libstegan._minimal_pixel_count(generic_conf_dict, generic_msg) == 13

def test_generate_dimensions_should_be_4_by_4():
    assert libstegan._generate_dimensions(generic_conf_dict, generic_msg) == (4, 4)

def test_pixeliterator_length():
    pi = libstegan.PixelIterator(generic_conf_dict, generic_img)
    assert len(list(pi)) == 16

def test_pixeliter_0_0_should_be_0_0():
    pi = libstegan.PixelIterator(generic_conf_dict, generic_img)
    zeroth_zeroth = next(pi)
    assert zeroth_zeroth[1] == 0 and zeroth_zeroth[1] == 0

def test_pixel_iter_0_0_should_be_red():
    pi = libstegan.PixelIterator(generic_conf_dict, generic_img)
    zeroth_zeroth = next(pi)
    assert zeroth_zeroth[0] == 'red'

def test_pixel_iter_0_1_should_be_whatever():
    pi = libstegan.PixelIterator(generic_conf_dict, generic_img)
    next(pi)
    zeroth_first = next(pi)
    assert zeroth_first[0] == 'whatever'

def test_pixel_iter_0_3_should_be_blue():
    pi = libstegan.PixelIterator(generic_conf_dict, generic_img)
    for x in range(4):
        pixel = next(pi)
    assert pixel[0] == 'blue'

def test_craft_pixel_letter_a_in_red():
    crafted_pixel = libstegan._craft_pixel('red', 'a', 0)
    assert chr(crafted_pixel[0]) == 'a'

def test_encode_decode_end_to_end():
    msg_before = 'Ala posiada zwierze z czterema lapkami i ogonem'
    msg_after = libstegan.encode(generic_conf_dict, msg_before)
    assert libstegan.decode(generic_conf_dict, msg_after).startswith(msg_before)

def test_encode_decode_with_long_frequency():
    msg = 'abcdefgh'
    another_conf_dict = {
        'red': True,
        'green': False,
        'blue': True,
        'frequency': 1027,
    }
    msg_after = libstegan.encode(another_conf_dict, msg)
    assert libstegan.decode(another_conf_dict, msg_after).startswith(msg)
