import pytest

from csiquant import si, SIUnit

def test_create_units():
    x = SIUnit.Unit(m=1)

    assert x.scale == 1
    assert x.m == 1

    x = SIUnit.Unit(0.001, m=1)
    assert x.scale == 0.001
    assert x.m == 1

    with pytest.raises(ValueError):
        x = SIUnit.Unit(0, m=1)

    with pytest.raises(ValueError):
        x = SIUnit.Unit(-1, m=1)

def test_hash_units():
    h1 = hash(si.meters)
    h2 = hash(si.millimeters)
    h3 = hash(SIUnit.Unit(m=1))
    h4 = hash(SIUnit.Unit(kg=1))
    assert h1 != h2
    assert h1 == h3
    assert h1 != h4
    assert h2 != h4

def test_cmp_units():


    assert si.millimeters < si.meters
    assert si.millimeters <= si.meters
    assert si.meters <= si.meters

    assert si.kilometers > si.meters
    assert si.kilometers >= si.meters
    assert si.meters >= si.meters

    assert not si.meters > si.meters
    assert not si.meters < si.meters

    with pytest.raises(ValueError):
        si.meters > si.micrograms

    with pytest.raises(ValueError):
        si.meters >= si.micrograms

    with pytest.raises(ValueError):
        si.meters < si.tonnes

    with pytest.raises(ValueError):
        si.meters <= si.tonnes

    with pytest.raises(TypeError):
        si.millimeters > None

    with pytest.raises(TypeError):
        si.meters < 1


def test_pack_units():
    a, b, c = si.millimeters.pack(1, 2, 3)

    assert a.quantity == 1
    assert a.units == si.millimeters

    assert b.quantity == 2
    assert b.units == si.millimeters

    assert c.quantity == 3
    assert c.units == si.millimeters


def test_unpack_units():
    a, b, c = si.meters.pack(1, 2, 3)

    aa, bb, cc = si.millimeters.unpack(a, b, c)

    assert aa == 1000
    assert bb == 2000
    assert cc == 3000

def test_mul_units():
    moment = si.newtons * si.meters

    assert moment.scale == 1
    assert moment.kg == 1
    assert moment.m == 2
    assert moment.s == -2

    moment = si.millinewtons * si.millimeters

    assert moment.scale == 1e-6
    assert moment.kg == 1
    assert moment.m == 2
    assert moment.s == -2

    with pytest.raises(TypeError):
        moment * None

    with pytest.raises(TypeError):
        None * moment

def test_div_units():
    linear_density = si.kilograms / si.meters

    assert linear_density.scale == 1
    assert linear_density.kg == 1
    assert linear_density.m == -1


def test_pow_units():
    volume = si.millimeters ** 3
    assert volume.scale == 1e-9
    assert volume.dimensions == si.millimeters.dimensions ** 3

def test_approx_units():

    x1 = SIUnit.Unit(1000.0000001)
    x2 = SIUnit.Unit(1000)

    #assert x1 != x2
    assert x1.approx(x2, rtol=1e-9, atol=0)
    assert x2.approx(x1, rtol=1e-9, atol=0)

    assert not x1.approx(x2, rtol=1e-12, atol=0)
    assert not x2.approx(x1, rtol=1e-12, atol=0)

    assert x1.approx(x2, rtol=0, atol=1e-6)
    assert x2.approx(x1, rtol=0, atol=1e-6)

    assert not x1.approx(x2, rtol=0, atol=1e-9)
    assert not x2.approx(x1, rtol=0, atol=1e-9)


def test_invert_units():
    x = ~si.millimeters

    assert x.scale == 1000
    assert x.m == -1


def test_compatible_units():
    assert si.meters.compatible(si.millimeters)
    assert not si.meters.compatible(si.kilograms)