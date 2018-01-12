import libstegan


def test_imported_correctly():
    assert 'RGBCycler' in libstegan.__dict__

def test_ascii_validation_true():
    msg = 'An ascii-only string :) ;>'
    assert libstegan._validate_ascii(msg) == True

def test_ascii_validation_false():
    msg = 'Żażółć gęślą żółtą jaźń'
    assert libstegan._validate_ascii(msg) == False
