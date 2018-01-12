import libstegan


generic_conf_dict =  {
    'red': True,
    'green': False,
    'blue': True,
    'frequency': 3
}


def test_imported_correctly():
    assert 'RGBCycler' in libstegan.__dict__

def test_ascii_validation_true():
    msg = 'An ascii-only string :) ;>'
    assert libstegan._validate_ascii(msg) == True

def test_ascii_validation_false():
    msg = 'Żażółć gęślą żółtą jaźń'
    assert libstegan._validate_ascii(msg) == False

def test_minimal_pixel_count_for_msg_len_5_and_freq_3():
    message = 'abcde'
    # I've done it by hand on a sheet of paper so I hope that's correct
    assert libstegan._minimal_pixel_count(generic_conf_dict, message) == 13
