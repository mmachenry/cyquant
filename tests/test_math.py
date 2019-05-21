import pytest

import math

from cyquant import si
from cyquant import qmath

def test_sin():
    expected = math.sin(math.pi / 2)

    actual = qmath.sin(math.pi / 2 * si.radians)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    actual = qmath.sin(90 * si.degrees)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    with pytest.raises(TypeError):
        qmath.sin(math.pi / 2)


def test_cos():
    expected = math.cos(math.pi)

    actual = qmath.cos(math.pi * si.radians)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    actual = qmath.cos(180 * si.degrees)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    with pytest.raises(TypeError):
        qmath.cos(math.pi)


def test_tan():
    expected = math.tan(math.pi / 4)

    actual = qmath.tan(math.pi / 4 * si.radians)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    actual = qmath.tan(45 * si.degrees)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    with pytest.raises(TypeError):
        qmath.tan(math.pi / 4)


def test_asin():

    expected = math.asin(1/2)

    y = 1 * si.meters
    h = 2 * si.meters

    actual = qmath.asin(y / h)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    h = 2000 * si.millimeters

    actual = qmath.asin(y / h)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    with pytest.raises(TypeError):
        qmath.asin(2)

    with pytest.raises(ValueError):
        qmath.asin(2 * si.unity)

def test_acos():
    expected = math.acos(1/2)
    x = 1 * si.meters
    h = 2 * si.meters

    actual = qmath.acos(x / h)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    x = 1000 * si.millimeters
    actual = qmath.acos(x / h)
    assert actual.is_of(si.unity.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    with pytest.raises(TypeError):
        qmath.acos(2)

    with pytest.raises(ValueError):
        qmath.acos(2 * si.unity)

def test_atan():
    pass

def test_atan2():

    xval = 2
    yval = -2

    expected = math.atan2(yval, xval)

    x = xval * si.meters
    y = yval * si.meters

    actual = qmath.atan2(y, x)

    assert actual.is_of(si.radians.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    y = y.cvt_to(si.millimeters)

    actual = qmath.atan2(y, x)

    assert actual.is_of(si.radians.dimensions)
    assert pytest.approx(1) == actual.units.scale
    assert pytest.approx(expected) == actual.quantity

    with pytest.raises(TypeError):
        qmath.atan2(5, 3)

    with pytest.raises(ValueError):
        qmath.atan2(0 * si.meters, 0 * si.meters)

    with pytest.raises(ValueError):
        qmath.atan2(1 * si.meters, 1 * si.kilograms)

def test_hypot():
    x = 1 * si.meters
    y = 2 * si.meters

    expected = (1 ** 2 + 2 ** 2) ** 0.5

    h = qmath.hypot(x, y)
    assert h.units == si.meters
    assert pytest.approx(expected) == h.quantity

    y = 2000 * si.millimeters
    h = qmath.hypot(x, y)
    assert h.units == si.millimeters
    assert pytest.approx(1000 * expected) == h.quantity