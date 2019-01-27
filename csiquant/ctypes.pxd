from libc.string cimport memcmp

cdef struct DData:
    double exponents[7]

cdef struct UData:
    double scale
    DData dimensions

cdef struct QData:
    double quantity
    UData units

cdef enum OPERAND:
    ERROR = 1
    UNIT = 2
    QUANTITY = 4

cdef inline void mul_ddata(DData& out, const DData& lhs, const DData& rhs):
    cdef int i

    for i in range(7):
        out.exponents[i] = lhs.exponents[i] + rhs.exponents[i]

cdef inline void div_ddata(DData& out, const DData& lhs, const DData& rhs):
    cdef int i

    for i in range(7):
        out.exponents[i] = lhs.exponents[i] - rhs.exponents[i]

cdef inline void pow_ddata(DData& out, const DData& lhs, double power):
    cdef int i

    for i in range(7):
        out.exponents[i] = lhs.exponents[i] * power

cdef inline bint eq_ddata(const DData& lhs, const DData& rhs):
    return memcmp(&lhs, &rhs, sizeof(DData)) == 0

cdef inline void mul_udata(UData& out, const UData& lhs, const UData& rhs):
    out.scale = lhs.scale * rhs.scale
    mul_ddata(out.dimensions, lhs.dimensions, rhs.dimensions)

cdef inline void div_udata(UData& out, const UData& lhs, const UData& rhs):
    out.scale = lhs.scale / rhs.scale
    div_ddata(out.dimensions, lhs.dimensions, rhs.dimensions)

cdef inline void pow_udata(UData& out, const UData& lhs, double power):
    out.scale = lhs.scale ** power
    pow_ddata(out.dimensions, lhs.dimensions, power)

cdef inline bint cmp_udata(int& out, const UData& lhs, const UData& rhs):
    if not eq_ddata(lhs.dimensions, rhs.dimensions):
        return 0

    if lhs.scale > rhs.scale:
        (&out)[0] = 1
    elif lhs.scale < rhs.scale:
        (&out)[0] = -1
    else:
        (&out)[0] = 0

    return 1

cdef inline void mul_qdata(QData& out, const QData& lhs, const QData& rhs):
    out.quantity = lhs.quantity * rhs.quantity
    mul_udata(out.units, lhs.units, rhs.units)

cdef inline void div_qdata(QData& out, const QData& lhs, const QData& rhs):
    out.quantity = lhs.quantity / rhs.quantity
    div_udata(out.units, lhs.units, rhs.units)

cdef inline void pow_qdata(QData& out, const QData& lhs, double rhs):
    out.quantity = lhs.quantity ** rhs
    pow_udata(out.units, lhs.units, rhs)

cdef inline bint add_qdata(QData& out, const QData& lhs, const QData& rhs):
    if not cvt_quantity(out, rhs, lhs.units):
        return 0
    out.quantity += lhs.quantity
    return 1

cdef inline bint sub_qdata(QData& out, const QData& lhs, const QData& rhs):
    if not cvt_quantity(out, rhs, lhs.units):
        return 0
    out.quantity = lhs.quantity - out.quantity
    return 1

cdef inline bint cvt_quantity(QData& out, const QData& src, const UData& units):
    if not extract_quantity(out.quantity, src, units):
        return 0
    out.units = units
    return 1

cdef inline bint extract_quantity(double& out, const QData& src, const UData& units):
    if not eq_ddata(src.units.dimensions, units.dimensions):
        return 0
    (&out)[0] = src.quantity * src.units.scale / units.scale
    return 1

cdef inline bint cmp_qdata(int& out, const QData& lhs, const QData& rhs):
    if not eq_ddata(lhs.units.dimensions, rhs.units.dimensions):
        return 0

    cdef lhs_norm = lhs.quantity * lhs.units.scale
    cdef rhs_norm = rhs.quantity * rhs.units.scale

    if lhs_norm > rhs_norm:
        (&out)[0] = 1
    elif lhs_norm < rhs_norm:
        (&out)[0] = -1
    else:
        (&out)[0] = 0


    return 1