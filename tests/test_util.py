import pytest

from cyquant import si, converter

def test_converter_strict():

    cvtr = converter(si.meters, promotes=False)

    q = cvtr(1 * si.meters)

    assert q.quantity == 1
    assert q.units == si.meters

    q = cvtr(1 * si.kilometers)

    assert q.quantity == 1000
    assert q.units == si.meters

    with pytest.raises(TypeError):
        q = cvtr(1)

    with pytest.raises(TypeError):
        q = cvtr(None)

    with pytest.raises(ValueError):
        q = cvtr(1 * si.kilograms)


    with pytest.raises(TypeError):
        cvtr = converter(None)

    with pytest.raises(TypeError):
        converter(object())

def test_converter_promiscuous():

    cvtr = converter(si.meters, promotes=True)

    q = cvtr(1 * si.meters)

    assert q.quantity == 1
    assert q.units == si.meters

    q = cvtr(1 * si.kilometers)

    assert q.quantity == 1000
    assert q.units == si.meters

    q = cvtr(1)

    assert q.quantity == 1
    assert q.units == si.meters

    with pytest.raises(TypeError):
        q = cvtr(None)

    with pytest.raises(ValueError):
        q = cvtr(1 * si.kilograms)

    with pytest.raises(TypeError):
        cvtr = converter(None, promotes=True)

    with pytest.raises(TypeError):
        cvtr = converter(object(), promotes=True)