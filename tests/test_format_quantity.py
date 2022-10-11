from cyquant import si, Quantity, SIUnit, Dimensions
from cyquant.format_quantity import show_quantity


def test_show_quantity():
	def _q(value: float, scale: float, dimensions: dict) -> Quantity:
		"""Helper function to create cyquant quantities for testing"""
		dims = {"kg": 0, "m": 0, "s": 0, "k": 0,
                    "a": 0, "mol": 0, "cd": 0}

		for dim in list(dimensions.keys()):
			if dim not in {'kg', 'm', 's', 'k', 'a', 'mol', 'cd'}:
				raise ValueError("Unrecognized Dimension")
		dims.update(dimensions)

		return Quantity(value, SIUnit(scale, Dimensions(**dims)))

	# (si unit, expected value)
	values = [
		(1 * si.nano,  '1.000e-09'),
		(1 * si.micro, '1.000e-06'),
		(1 * si.milli, '1.000e-03'),
		(1 * si.centi, '1.000e-02'),
		(1 * si.deci, '1.000e-01'),
		(1 * si.unity, '1.0'),
		(1 * si.deca, '1.000e+01'),
		(1 * si.hecta, '1.000e+02'),
		(1 * si.kilo, '1.000e+03'),
		(1 * si.mega,  '1.000e+06'),
		(1 * si.giga,  '1.000e+09'),
		(1 * si.tera,  '1.000e+12'),
		(1 * si.meters,    '1.0 m'),
		(1 * si.kilograms, '1.0 kg'),
		(1 * si.seconds,   '1.0 s'),
		(1 * si.kelvin,    '1.0 K'),
		(1 * si.amperes,   '1.0 A'),
		(1 * si.mols,     '1.0 mols'),
		(1 * si.candelas, '1.0 cd'),
		(1 * si.radians,  '1.0'),
		(1 * si.radians,  '1.0'),
		(1 * si.degrees,  '1.745e-02'),
		(1 * si.hertz,   '1.0 [1]/[s]'),
		(1 * si.newtons, '1.000e+00 N'),
		(1 * si.pascals, '1.000e+00 Pa'),
		(1 * si.joules,  '1.000e+00 J (N*m)'),
		(1 * si.watts,   '1.000e+00 W'),
		(1 * si.coulombs, '1.000e+00 C'),
		(1 * si.volts,   '1.000e+00 V'),
		(1 * si.farads,  '1.000e+00 F'),
		(1 * si.ohms,    '1.000e+00 Ω'),
		(1 * si.siemens, '1.000e+00 S'),
		(1 * si.webers, '1.000e+00 Wb'),
		(1 * si.teslas, '1.000e+00 T'),
		(1 * si.henrys, '1.000e+00 H'),
		(1 * si.lumens, '1.0 cd'),
		(1 * si.becquerels, '1.0 [1]/[s]'),
		(1 * si.sieverts,   '1.000e+00 [J]/[kg]'),
		(1 * si.katals,     '1.000e+00 [mol]/[s]'),
		(1 * si.nanometers, '1.0 nm'),
		(1 * si.micrometers, '1.0 µm'),
		(1 * si.millimeters, '1.0 mm'),
		(1 * si.centimeters, '1.0 cm'),
		(1 * si.decimeters, '1.0 dm'),
		(1 * si.decameters, '1.0 dam'),
		(1 * si.hectameters, '1.0 hm'),
		(1 * si.kilometers, '1.0 km'),
		(1 * si.liters,    '1.000e-03 [(m^3)]'),
		(1 * si.grams,     '1.0 g'),
		(1 * si.milligrams, '1.0 mg'),
		(1 * si.micrograms, '1.0 µg'),
		(1 * si.tonnes,    '1.0 Mg'),
		(1 * si.kilotonnes, '1.0 Gg'),
		(1 * si.nanoseconds, '1.0 ns'),
		(1 * si.microseconds, '1.0 µs'),
		(1 * si.milliseconds, '1.0 ms'),
		(1 * si.minutes,      '6.000e+01 s'),
		(1 * si.days,   '8.640e+04 s'),
		(1 * si.weeks,   '6.048e+05 s'),
		(1 * si.years,   '3.154e+07 s'),
		(1 * si.gals,   '1.000e-02 [m]/[(s^2)]'),  # not gal -> galileos
		(1 * si.g_0, '9.807e+00 [m]/[(s^2)]'),
		(1 * si.micropascals, '1.000e-06 Pa'),
		(1 * si.millipascals, '1.000e-03 Pa'),
		(1 * si.kilopascals, '1.000e+03 Pa'),
		(1 * si.megapascals, '1.000e+06 Pa'),
		(1 * si.gigapascals, '1.000e+09 Pa'),
		(1 * si.millijoules, '1.000e-03 J (N*m)'),
		(1 * si.kilojoules,  '1.000e+03 J (N*m)'),
		(1 * si.megajoules,  '1.000e+06 J (N*m)'),
		(1 * si.gigajoules,  '1.000e+09 J (N*m)'),
		(1 * si.terajoules,  '1.000e+12 J (N*m)'),
		(1 * si.milliwatts,  '1.000e-03 W'),
		(1 * si.kilowatts,   '1.000e+03 W'),
		(1 * si.megawatts,   '1.000e+06 W'),
		(1 * si.gigawatts,   '1.000e+09 W'),
		(1 * si.terawatts,   '1.000e+12 W'),
		(1 * si.millivolts,   '1.000e-03 V'),
		(1 * si.kilovolts,   '1.000e+03 V'),
		(1 * si.megavolts,   '1.000e+06 V'),
		(1 * si.gigavolts,   '1.000e+09 V'),
		(1 * si.teravolts,   '1.000e+12 V'),
		(1 * si.micronewtons,   '1.000e-06 N'),
		(1 * si.millinewtons,   '1.000e-03 N'),
		(1 * si.kilonewtons,   '1.000e+03 N'),
		(1 * si.newton_meters,   '1.000e+00 J (N*m)'),
		(1 * si.kilonewton_meters,   '1.000e+03 J (N*m)'),
		(1 * si.meters_per_second,   '1.000e+00 [m]/[s]'),
		# Extra Tests #
		(_q(0.0, 0.017453, {}), '0.000e+00'),
		(_q(1.25, 10**-3, {"m": 1}), '1.25 mm'),
	]

	# Testing different units
	# val = 1 * si.gigapascals
	# print(val)
	# print(show_quantity(val), type(show_quantity(val)))

	for value in values:
		tested = show_quantity(value[0])
		expected = value[1]
		error = f"{tested} != Expected Value: {expected} "
		assert tested == expected, error
