cimport csiquant.ctypes as c
cimport csiquant.dimensions as d
import csiquant.dimensions as d

cdef class SIUnit:
    cdef c.UData data

    cpdef SIUnit exp(SIUnit self, double power)

cdef class Quantity:
    cdef c.QData data

    cpdef bint is_of(Quantity self, d.Dimensions dimensions)
    cpdef double get_as(Quantity self, SIUnit units)
    cpdef Quantity cvt_to(Quantity self, SIUnit units)
    cpdef Quantity round_to(Quantity self, SIUnit units)

    #TODO: think abuot how best to handle approximation

    cpdef Quantity exp(Quantity self, double power)


cdef inline Quantity mul_quantities(const c.QData& lhs, const c.QData& rhs):
    cdef Quantity ret = Quantity.__new__(Quantity)
    c.mul_qdata(ret.data, lhs, rhs)
    return ret

cdef inline SIUnit mul_units(const c.UData& lhs, const c.UData& rhs):
    cdef SIUnit ret = SIUnit.__new__(SIUnit)
    c.mul_udata(ret.data, lhs, rhs)
    return ret

cdef inline Quantity div_quantities(const c.QData& lhs, const c.QData& rhs):
    cdef Quantity ret = Quantity.__new__(Quantity)
    c.div_qdata(ret.data, lhs, rhs)
    return ret

cdef inline SIUnit div_units(const c.UData& lhs, const c.UData& rhs):
    cdef SIUnit ret = SIUnit.__new__(SIUnit)
    c.div_udata(ret.data, lhs, rhs)
    return ret

# parsing functions

cdef inline c.OPERAND parse_uoperand(c.QData& out, object py_obj):
    op_type = type(py_obj)
    if op_type is float or op_type is int:
        out.quantity = py_obj
        out.units.scale = 1.0
        out.units.dimensions.data[:] = [0,0,0,0,0,0,0]
        return c.QUANTITY
    elif op_type is SIUnit:
        return extract_udata(out.units, py_obj)
    elif op_type is Quantity:
        return extract_qdata(out, py_obj)
    else:
        return c.ERROR


cdef inline c.OPERAND parse_qoperand(c.QData& out, object py_obj):
    op_type = type(py_obj)
    if op_type is Quantity:
        return extract_qdata(out, py_obj)
    elif op_type is float or op_type is int:
        out.quantity = py_obj
        out.units.scale = 1.0
        out.units.dimensions.data[:] = [0,0,0,0,0,0,0]
        return c.QUANTITY
    return c.ERROR


cdef inline c.OPERAND extract_udata(c.UData& out, SIUnit py_obj):
    (&out)[0] = py_obj.data
    return c.UNIT


cdef inline c.OPERAND extract_qdata(c.QData& out, Quantity py_obj):
    (&out)[0] = py_obj.data
    return c.QUANTITY