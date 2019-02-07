import pytest
import copy

from cyquant import si, Quantity, SIUnit, Dimensions

def test_create_quantity():
    q1 = Quantity(1, SIUnit.Unit(1, m=1))

    assert q1.quantity == 1
    units = q1.units
    assert units.scale == 1
    dimensions = units.dimensions
    assert dimensions.m == 1
    assert dimensions.kg == 0
    assert dimensions.s == 0
    assert dimensions.k == 0
    assert dimensions.a == 0
    assert dimensions.mol == 0
    assert dimensions.cd == 0

def test_copy_quantity():
    in_m = 1000 * si.meters

    copied = copy.copy(in_m)
    assert copied.quantity == 1000
    assert copied.units == si.meters

    copied = copy.deepcopy(in_m)
    assert copied.quantity == 1000
    assert copied.units == si.meters

def test_extract_quantity():
    in_m = 1000 * si.meters

    assert in_m.get_as(si.kilometers) == 1
    assert in_m.get_as(si.millimeters) == 1000000

    with pytest.raises(ValueError):
        in_m.get_as(si.volts)

    with pytest.raises(TypeError):
        in_m.get_as(in_m)

def test_extract_rounded_quantity():
    in_m = 1025 * si.meters

    assert in_m.round_as(si.kilometers) == 1

def test_cvt_quantity():
    in_m = 1000 * si.meters

    in_mm = in_m.cvt_to(si.millimeters)
    assert in_mm.quantity == 1000000

    in_km = in_m.cvt_to(si.kilometers)
    assert in_km.quantity == 1

    with pytest.raises(ValueError):
        in_m.cvt_to(si.volts)

    with pytest.raises(TypeError):
        in_m.cvt_to(1)

def test_round_quantity():
    in_m = 1001 * si.meters

    in_mm = in_m.round_to(si.millimeters)
    assert in_mm.quantity == 1001000

    in_km = in_m.round_to(si.kilometers)
    assert in_km.quantity == 1

    with pytest.raises(ValueError):
        in_m.round_to(si.milligrams)

    with pytest.raises(TypeError):
        in_m.round_to(1000)

def test_r_approx_quantity():
    in_gpa = 210 * si.gigapascals
    in_kpa = 210000002 * si.kilopascals
    in_pa = 210000000002 * si.pascals

    assert in_gpa.r_approx(in_pa)
    assert in_pa.r_approx(in_gpa)

    assert not in_gpa.r_approx(in_kpa)
    assert not in_kpa.r_approx(in_gpa)

    assert in_gpa.r_approx(in_kpa, 1e-8)
    assert in_kpa.r_approx(in_gpa, 1e-8)

def test_a_approx_quantity():
    in_gpa = 210 * si.gigapascals
    in_kpa = 210000001 * si.kilopascals
    in_pa  = 210000000001 * si.pascals

    assert in_gpa.a_approx(in_pa, atol=1)
    assert in_pa.a_approx(in_gpa, atol=1)

    assert not in_gpa.a_approx(in_pa)
    assert not in_pa.a_approx(in_gpa)

    other = 210 * si.gigawatts

    with pytest.raises(ValueError):
        other.a_approx(in_gpa)

    with pytest.raises(ValueError):
        in_gpa.a_approx(other)


def test_q_approx_quantity():
    in_mm = 1000001 * si.millimeters
    in_km = 1 * si.kilometers

    assert in_mm.q_approx(in_km, 2 * si.millimeters)
    assert in_km.q_approx(in_mm, 2 * si.millimeters)

    assert not in_mm.q_approx(in_km, 1 * si.micrometers)
    assert not in_km.q_approx(in_mm, 1 * si.micrometers)

    with pytest.raises(ValueError):
        in_km.q_approx(in_mm, 1 * si.millivolts)

    with pytest.raises(ValueError):
        in_km.q_approx(1000 * si.volts, 1 * si.millimeters)

def test_is_of_quantity():
    in_m = 1000 * si.meters

    assert in_m.is_of(si.meters.dimensions)
    assert in_m.is_of(si.millimeters.dimensions)

    assert not in_m.is_of(si.milligrams.dimensions)

    in_u = 1000 * si.unity
    with pytest.raises(TypeError):
        assert in_u.is_of(None)

    with pytest.raises(TypeError):
        in_m.is_of(1)

def test_hash_quantity():
    in_m = 1 * si.meters
    in_mm = 1000 * si.millimeters

    m_hash = hash(in_m)
    mm_hash = hash(in_mm)

    assert m_hash == mm_hash

def test_eq_quantity():
    q1 = 1 * si.meters
    q2 = 1000 * si.millimeters
    q3 = 2 * si.meters
    q4 = 2000 * si.millimeters
    q5 = 1 * si.kilograms

    assert q1 == q2
    assert q3 == q4

    assert q1 != q3
    assert q2 != q4

    assert q1 != q4
    assert q3 != q2

    assert q1 != q5

def test_order_quantity():
    q1 = 1 * si.meters
    q2 = 2 * si.meters
    q3 = 2000 * si.millimeters
    q4 = 2 * si.volts

    assert q1 < q2
    assert q1 < q3
    assert not q2 < q3

    assert q1 <= q2
    assert q2 <= q3

    assert q2 > q1
    assert q3 > q1
    assert not q3 > q2

    assert q2 >= q1
    assert q3 >= q2

    with pytest.raises(ValueError):
        q1 < q4

    with pytest.raises(ValueError):
        q1 <= q4

    with pytest.raises(ValueError):
        q1 > q4

    with pytest.raises(ValueError):
        q1 >= q4

    with pytest.raises(TypeError):
        q1 < None

    with pytest.raises(TypeError):
        q1 > None

    with pytest.raises(TypeError):
        q1 >= None

    with pytest.raises(TypeError):
        q1 <= None

    with pytest.raises(TypeError):
        q1 < 1

    with pytest.raises(TypeError):
        q1 > 1

    with pytest.raises(TypeError):
        q1 <= 1

    with pytest.raises(TypeError):
        q1 >= 1

def test_float_quantity():
    q1 = 1 * si.meters
    q2 = 1 * si.volts
    q3 = 1000 * si.millimeters

    assert float(q1) == 1
    assert float(q2) == 1
    assert float(q3) == 1000

def test_int_quantity():
    q1 = 1 * si.meters
    q2 = 1 * si.volts
    q3 = 1000 * si.millimeters

    assert int(q1) == 1
    assert int(q2) == 1
    assert int(q3) == 1000

def test_truth_quantity():
    q0 = 0 * si.meters
    q1 = 1 * si.meters
    q2 = 1 * si.volts
    q3 = 1000 * si.millimeters

    assert not q0
    assert q1
    assert q2
    assert q3

def test_abs_quantity():
    q0 = 0 * si.meters
    q1 = 1 * si.meters
    q2 = -1 * si.meters

    assert q0 == abs(q0)
    assert q1 == abs(q1)
    assert q1 == abs(q2)

def test_invert_quantity():
    q0 = 0 * si.meters

    q1 = 0.5 * si.meters
    q11 = 2 / si.meters

    q2 = 1 * si.meters
    q22 = 1 / si.meters

    q3 = 2 * si.meters
    q33 = 0.5 / si.meters

    with pytest.raises(ZeroDivisionError):
        q0 = ~q0

    assert q11 == ~q1
    assert q22 == ~q2
    assert q33 == ~q3


def test_neg_quantity():
    q0 = 0 * si.meters
    qp = 1 * si.meters
    qn = -1 * si.meters

    assert q0 == -q0
    assert qp == -qn
    assert -qp == qn

def test_pow_quantity():
    in_m = 1 * si.meters

    in_m3 = in_m ** 3
    assert in_m3.quantity == 1
    assert in_m3.units.scale == 1
    assert in_m3.units.m == 3

    in_mm = 1000 * si.millimeters

    in_mm3 = in_mm ** 3
    assert in_mm3.quantity == 1e9
    assert in_mm3.units.scale == 1e-9
    assert in_mm3.units.m == 3

    assert in_m3 == in_mm3

def test_mul_quantity():
    stress = 0.1 * si.gigapascals
    area = 100 * si.millimeters ** 2
    force = stress * area

    assert force.quantity == 10
    assert force.units.scale == 1e3

    assert force.get_as(si.newtons) == 10000

def test_div_quantity():
    force = 10 * si.kilonewtons
    area = 100 * si.millimeters ** 2
    stress = force / area

    assert stress.quantity == 0.1
    assert stress.units.scale == 1e9

    assert stress.get_as(si.pascals) == 1e8

    zero_area = 0 * si.millimeters ** 2
    with pytest.raises(ZeroDivisionError):
        force / zero_area


def test_add_quantity():
    in_m = 1 * si.meters
    in_mm = 1000 * si.millimeters

    out = in_m + in_mm

    assert out.quantity == 2000
    assert out.units.scale == 0.001
    assert out.units.dimensions == in_m.units.dimensions

    out = in_mm + in_m

    assert out.quantity == 2000
    assert out.units.scale == 0.001
    assert out.units.dimensions == in_m.units.dimensions


    with pytest.raises(ValueError):
        in_m + 10 * si.kilograms

    with pytest.raises(ValueError):
        10 * si.kilograms + in_mm

    with pytest.raises(TypeError):
        in_m + None

    with pytest.raises(TypeError):
        None + in_m

    with pytest.raises(TypeError):
        in_m + 1

    with pytest.raises(TypeError):
        1 + in_mm

def test_sub_quantity():
    in_m = 1 * si.meters
    in_mm = 1000 * si.millimeters

    out = in_m - in_mm

    assert out.quantity == 0
    assert out.units.scale == 0.001
    assert out.units.dimensions == in_m.units.dimensions

    out = in_mm - in_m

    assert out.quantity == 0
    assert out.units.scale == 0.001
    assert out.units.dimensions == in_m.units.dimensions

    with pytest.raises(ValueError):
        in_m + 10 * si.kilograms

    with pytest.raises(ValueError):
        10 * si.kilograms + in_mm

    with pytest.raises(TypeError):
        in_m + None

    with pytest.raises(TypeError):
        None + in_m

    with pytest.raises(TypeError):
        in_m + 1

    with pytest.raises(TypeError):
        1 + in_mm

