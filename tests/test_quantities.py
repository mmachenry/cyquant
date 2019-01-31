import pytest

from csiquant import si

def test_create_quantity():
    assert False

def test_copy_quantity():
    assert False

def test_extract_quantity():
    assert False

def test_cvt_quantity():
    assert False

def test_round_quantity():
    assert False

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
    assert False

def test_hash_quantity():
    assert False

def test_ne_quantity():
    assert False

def test_order_quantity():
    assert False

def test_float_quantity():
    assert False

def test_truth_quantity():
    assert False

def test_abs_quantity():
    assert False

def test_invert_quantity():
    assert False

def test_neg_quantity():
    assert False

def test_pow_quantity():
    assert False

def test_mul_quantity():
    assert False

def test_div_quantity():
    assert False

def test_add_quantity():
    assert False

def test_sub_quantity():
    assert False

