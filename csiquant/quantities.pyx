cimport csiquant.ctypes as c
cimport csiquant.dimensions as d
import csiquant.dimensions as d

from libc.math cimport round, fabs

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

    def __init__(SIUnit self, double scale=1.0, d.Dimensions dims=d.dimensionless_t):
        self.data.scale = scale
        self.data.dimensions = dims.data

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
        ret.data.dimensions = d.dimensionless_t
        c.div_udata(ret.data, ret.data, self.data)
        return ret

    def __pow__(lhs, rhs, modulo):
        return lhs.exp(rhs)

    cpdef SIUnit exp(SIUnit self, double power):
        cdef SIUnit ret = SIUnit.__new__(SIUnit)
        c.pow_udata(ret.data, self.data, power)
        return ret

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

    def __pow__(self, power, modulo):
        return self.exp(power)

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

    def __bool__(Quantity self):
        return bool(self.data.quantity)

    def __float__(Quantity self):
        return float(self.data.quantity)

    cpdef Quantity exp(Quantity self, double power):
        cdef Quantity ret = Quantity.__new__(Quantity)
        c.pow_qdata(ret.data, self.data, power)
        return ret

    def __repr__(self):
        return 'Quantity(%f, %r)' % (self.quantity, self.units)