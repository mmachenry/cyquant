#!python
#cython: language_level=3

cimport csiquant.ctypes as c
cimport csiquant.dimensions as d
import csiquant.dimensions as d

from libc.math cimport round, fabs, fmax

cdef class SIUnit:

    @staticmethod
    def Unit(scale=1, kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
        return SIUnit(scale, d.Dimensions(kg, m, s, k, a, mol, cd))

    @property
    def scale(self):
        return self.data.scale

    @property
    def dimensions(self):
        cdef d.Dimensions dims = d.Dimensions.__new__(d.Dimensions)
        dims.data = self.data.dimensions
        return dims

    @property
    def kg(self):
        return self.data.dimensions.exponents[0]

    @property
    def m(self):
        return self.data.dimensions.exponents[1]

    @property
    def s(self):
        return self.data.dimensions.exponents[2]

    @property
    def k(self):
        return self.data.dimensions.exponents[3]

    @property
    def a(self):
        return self.data.dimensions.exponents[4]

    @property
    def mol(self):
        return self.data.dimensions.exponents[5]

    @property
    def cd(self):
        return self.data.dimensions.exponents[6]

    def __init__(SIUnit self, double scale=1.0, d.Dimensions dims=d.dimensionless_t):
        if scale <= 0:
            raise ValueError("scale must be greater than 0")
        self.data.scale = scale
        self.data.dimensions = dims.data

    """
    Wrapping Methods
    """

    def pack(SIUnit self, *args):
        return self.quantities(args)

    def unpack(SIUnit self, *args):
        return self.values(args)

    def quantities(SIUnit self, iterable):
        for value in iterable:
            yield self.promote(value)

    def values(SIUnit self, iterable):
        for quantity in iterable:
            yield self.demote(quantity)

    cpdef promote(SIUnit self, double value):
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = value
        ret.data.units = self.data
        return ret

    cpdef demote(SIUnit self, Quantity value):
        cdef double ret
        if not c.extract_quantity(ret, value.data, self.data):
            raise ValueError("unit mismatch")
        return ret

    __call__ = quantities

    """
    Comparison Methods
    """

    def __eq__(lhs, rhs):
        if not type(lhs) is SIUnit:
            return NotImplemented
        if not type(rhs) is SIUnit:
            return NotImplemented
        try:
            return lhs.cmp(rhs) == 0
        except ValueError:
            return NotImplemented

    cpdef int cmp(SIUnit self, SIUnit other):
        cdef int signum
        if not c.cmp_udata(signum, self.data, other.data):
            raise ValueError("units mismatch")
        return signum

    """
    Arithmetic Methods
    """

    def __mul__(lhs, rhs):
        cdef c.QData lhs_data, rhs_data
        cdef int code
        code = parse_uoperand(lhs_data, lhs) | parse_uoperand(rhs_data, rhs)
        if code & c.ERROR:
            return NotImplemented
        if code & c.QUANTITY:
            return mul_quantities(lhs_data, rhs_data)
        return mul_units(lhs_data.units, rhs_data.units)


    def __truediv__(lhs, rhs):
        cdef c.QData lhs_data, rhs_data
        cdef int code
        code = parse_uoperand(lhs_data, lhs) | parse_uoperand(rhs_data, rhs)
        if code & c.ERROR:
            return NotImplemented
        if code & c.QUANTITY:
            return div_quantities(lhs_data, rhs_data)
        return div_units(lhs_data.units, rhs_data.units)

    def __invert__(self):
        cdef SIUnit ret = SIUnit.__new__(SIUnit)
        ret.data.scale = 1.0
        ret.data.dimensions.exponents[:] = [0,0,0,0,0,0,0]
        c.div_udata(ret.data, ret.data, self.data)
        return ret

    def __pow__(lhs, rhs, modulo):
        if type(lhs) is not SIUnit:
            raise TypeError("Expected SIUnit ** Number")
        return lhs.exp(rhs)


    cpdef SIUnit exp(SIUnit self, double power):
        cdef SIUnit ret = SIUnit.__new__(SIUnit)
        c.pow_udata(ret.data, self.data, power)
        return ret

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return self

    def __repr__(self):
        return 'SIUnit(%f, %r)' % (self.scale, self.dimensions)

cdef class Quantity:

    @property
    def quantity(self):
        return self.data.quantity

    @property
    def units(self):
        cdef SIUnit units = SIUnit.__new__(SIUnit)
        units.data = self.data.units
        return units

    def __init__(Quantity self, double quantity, SIUnit units):
        self.data.quantity = quantity
        self.data.units = units.data

    cpdef bint is_of(Quantity self, d.Dimensions dims):
        return c.eq_ddata(self.data.units.dimensions, dims.data)

    cpdef double get_as(Quantity self, SIUnit units):
        cdef double value
        if not c.extract_quantity(value, self.data, units.data):
            raise ValueError("units mismatch")
        return value

    cpdef Quantity cvt_to(Quantity self, SIUnit units):
        if c.eq_ddata(self.data.units.dimensions, units.data.dimensions):
            return self

        cdef Quantity ret = Quantity.__new__(Quantity)
        c.cvt_quantity(ret.data, self.data, units.data)
        return ret

    cpdef Quantity round_to(Quantity self, SIUnit units):
        cdef Quantity ret = Quantity.__new__(Quantity)
        c.cvt_quantity(ret.data, self.data, units.data)
        ret.data.quantity = round(ret.data.quantity)
        return ret

    """
    Comparison Methods
    """

    def __eq__(lhs, rhs):
        if type(lhs) is not Quantity:
            return NotImplemented
        if type(rhs) is not Quantity:
            return NotImplemented
        try:
            return lhs.cmp(rhs) == 0
        except ValueError:
            return NotImplemented

    def __ne__(lhs, rhs):
        return not lhs == rhs

    def __lt__(lhs, rhs):
        return lhs.cmp(rhs) < 0

    def __le__(lhs, rhs):
        return lhs.cmp(rhs) <= 0

    def __gt__(lhs, rhs):
        return lhs.cmp(rhs) > 0

    def __ge__(lhs, rhs):
        return lhs.cmp(rhs) >= 0

    cpdef int cmp(Quantity self, Quantity other):
        cdef int signum
        if not c.cmp_qdata(signum, self.data, other.data):
            raise ValueError('unit mismatch')
        return signum

    cpdef bint compatible(Quantity self, Quantity other):
        return c.eq_ddata(self.data.units.dimensions, other.data.units.dimensions)

    cpdef r_approx(Quantity self, Quantity other, double rtol=1e-9):
        cdef c.UData norm_units
        if self.data.units.scale < other.data.units.scale:
            norm_units = self.data.units
        else:
            norm_units = other.data.units

        cdef double self_norm, other_norm, epsilon
        if not c.extract_quantity(self_norm, self.data, norm_units):
            raise ValueError("unit mismatch")
        if not c.extract_quantity(other_norm, other.data, norm_units):
            raise ValueError("unit mismatch")

        epsilon = fmax(1, fmax(self_norm, other_norm)) * rtol
        return fabs(self_norm - other_norm) <= fabs(epsilon)

    cpdef a_approx(Quantity self, Quantity other, double atol=1e-6):
        cdef c.UData norm_units
        if self.data.units.scale < other.data.units.scale:
            norm_units = self.data.units
        else:
            norm_units = other.data.units

        cdef double self_norm, other_norm
        if not c.extract_quantity(self_norm, self.data, norm_units):
            raise ValueError("unit mismatch")
        if not c.extract_quantity(other_norm, other.data, norm_units):
            raise ValueError("unit mismatch")

        return fabs(self_norm - other_norm) <= fabs(atol)

    cpdef q_approx(Quantity self, Quantity other, Quantity qtol):
        cdef double self_val, other_val
        if not c.extract_quantity(self_val, self.data, qtol.data.units):
            raise ValueError("unit mismatch")
        if not c.extract_quantity(other_val, other.data, qtol.data.units):
            raise ValueError("unit mismatch")
        return fabs(self_val - other_val) <= fabs(qtol.data.quantity)

    """
    Arithmetic Methods
    """

    def __add__(Quantity lhs, Quantity rhs):
        cdef Quantity ret = Quantity.__new__(Quantity)
        if not c.add_qdata(ret.data, lhs.data, rhs.data):
            raise ValueError("units mismatch")
        return ret

    def __sub__(Quantity lhs, Quantity rhs):
        cdef Quantity ret = Quantity.__new__(Quantity)
        if not c.sub_qdata(ret.data, lhs.data, rhs.data):
            raise ValueError("units mismatch")
        return ret

    def __mul__(lhs, rhs):
        cdef Quantity ret = Quantity.__new__(Quantity)
        cdef c.QData other
        cdef int code
        code = parse_qoperand(ret.data, lhs) | parse_qoperand(other, rhs)
        if code & c.ERROR:
            return NotImplemented
        c.mul_qdata(ret.data, ret.data, other)
        return ret

    def __truediv__(lhs, rhs):
        cdef Quantity ret = Quantity.__new__(Quantity)
        cdef c.QData other
        cdef int code
        code = parse_qoperand(ret.data, lhs) | parse_qoperand(other, rhs)
        if code & c.ERROR:
            return NotImplemented
        c.div_qdata(ret.data, ret.data, other)
        return ret

    def __pow__(lhs, rhs, modulo):
        if type(lhs) is not Quantity:
            raise TypeError("Expected Quantity ** Number")
        return lhs.exp(rhs)

    def __neg__(Quantity self):
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = -self.data.quantity
        ret.data.units = self.data.units
        return self

    def __invert__(self):
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = 1.0
        ret.data.units.scale = 1
        ret.data.units.dimensions = d.dimensionless_t
        c.div_qdata(ret.data, ret.data, self.data)
        return ret

    def __abs__(Quantity self):
        if self.data.quantity >= 0:
            return self
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = fabs(self.data.quantity)
        ret.data.units = self.data.units
        return ret

    cpdef Quantity exp(Quantity self, double power):
        cdef Quantity ret = Quantity.__new__(Quantity)
        c.pow_qdata(ret.data, self.data, power)
        return ret

    def __bool__(Quantity self):
        return bool(self.data.quantity)

    def __float__(Quantity self):
        return float(self.data.quantity)

    def __int__(Quantity self):
        return int(self.data.quantity)

    def __hash__(Quantity self):
        cdef double normalized = self.data.quantity * self.data.units.scale
        qtuple = (normalized, self.data.units.dimensions)
        return hash(qtuple)

    def __repr__(self):
        return 'Quantity(%f, %r)' % (self.quantity, self.units)