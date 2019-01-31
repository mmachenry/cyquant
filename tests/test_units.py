import pytest

from csiquant import si

def test_create_units():
    x = 1 * si.meters

    assert x.quantity == 1
    assert x.units == si.meters

def test_hash_units():
    assert False

def test_cmp_units():
    assert False

def test_pack_units():
    assert False

def test_unpack_units():
    assert False

def test_mul_units():
    assert False

def test_div_units():
    assert False

def test_pow_units():
    assert False

def test_approx_units():
    assert False

def test_invert_units():
    assert False

def test_compatible_units():
    assert False