import pytest

from csiquant import si

def test_create_units():
    x = 1 * si.meters

    assert x.quantity == 1
    assert x.units == si.meters