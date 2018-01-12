import libstegan


generic_msg = 'abcde'
generic_conf_dict =  {
    'red': True,
    'green': False,
    'blue': True,
    'frequency': 3
}


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

def test_pixeliter_length():
    pi = libstegan.PixelIter(generic_conf_dict, generic_msg)
    assert len(list(pi)) == 16

def test_pixeliter_0_0_should_be_0_0():
    pi = libstegan.PixelIter(generic_conf_dict, generic_msg)
    zeroth_zeroth = next(pi)
    assert zeroth_zeroth[1] == 0 and zeroth_zeroth[1] == 0

def test_pixel_iter_0_0_should_be_red():
    pi = libstegan.PixelIter(generic_conf_dict, generic_msg)
    zeroth_zeroth = next(pi)
    assert zeroth_zeroth[0] == 'red'

def test_pixel_iter_0_1_should_be_whatever():
    pi = libstegan.PixelIter(generic_conf_dict, generic_msg)
    next(pi)
    zeroth_first = next(pi)
    assert zeroth_first[0] == 'whatever'

def test_pixel_iter_0_3_should_be_blue():
    pi = libstegan.PixelIter(generic_conf_dict, generic_msg)
    for x in range(4):
        pixel = next(pi)
    assert pixel[0] == 'blue'

def test_pixel_iter_3_3_should_be_empty():
    # its index is dividable by 3, but message should already be printed by now
    pi = libstegan.PixelIter(generic_conf_dict, generic_msg)
    for x in range(4*4):
        pixel = next(pi)
    assert pixel[0] == 'whatever'
