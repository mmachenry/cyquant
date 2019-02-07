import pytest

from cyquant.dimensions import Dimensions

def test_create_dimensions():
    dims = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)
    assert dims.kg == 1
    assert dims.m == 2
    assert dims.s == 3
    assert dims.k == 4
    assert dims.a == 5
    assert dims.mol == 6
    assert dims.cd == 7

def test_cmp_dimensions():
    dims1 = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)
    dims2 = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)
    dims3 = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=0)

    assert dims1 == dims1
    assert dims1 == dims2
    assert dims2 == dims1

    assert dims1 != dims3
    assert dims3 != dims1

    assert dims1 != None

    with pytest.raises(TypeError):
        dims1 > dims2


def test_mul_dimensions():
    dims = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)

    new_dims = dims * dims

    assert new_dims.kg == 2
    assert new_dims.m == 4
    assert new_dims.s == 6
    assert new_dims.k == 8
    assert new_dims.a == 10
    assert new_dims.mol == 12
    assert new_dims.cd == 14

    with pytest.raises(TypeError):
        new_dims * 2

    with pytest.raises(TypeError):
        2 * new_dims

def test_div_dimensions():
    dims = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)

    new_dims = dims / dims

    assert new_dims.kg == 0
    assert new_dims.m == 0
    assert new_dims.s == 0
    assert new_dims.k == 0
    assert new_dims.a == 0
    assert new_dims.mol == 0
    assert new_dims.cd == 0

    with pytest.raises(TypeError):
        new_dims / 2

    with pytest.raises(TypeError):
        2 / new_dims

def test_pow_dimensions():
    dims = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)

    new_dims = dims ** 3

    assert new_dims.kg == 3
    assert new_dims.m == 6
    assert new_dims.s == 9
    assert new_dims.k == 12
    assert new_dims.a == 15
    assert new_dims.mol == 18
    assert new_dims.cd == 21

    with pytest.raises(TypeError):
        3 ** dims

    with pytest.raises(TypeError):
        dims ** None

def test_hash_dimensions():
    dims1 = Dimensions()
    dims2 = Dimensions()

    dims3 = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)
    dims4 = Dimensions(kg=1, m=2, s=3, k=4, a=5, mol=6, cd=7)

    assert hash(dims1) == hash(dims2)
    assert hash(dims3) == hash(dims4)

    assert hash(dims1) != hash(dims3)
    assert hash(dims2) != hash(dims4)