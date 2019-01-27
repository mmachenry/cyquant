from setuptools import setup
from setuptools.extension import Extension


from Cython.Distutils import build_ext

extensions = [
    Extension(
        "csiquant.dimensions",
        sources=[
            "csiquant/dimensions.pyx"
        ],
        language='c++'
    ),
    Extension(
        "csiquant.quantities",
        sources=[
            "csiquant/quantities.pyx"
        ],
        language='c++'
    )
]

setup(
    name='csiquant',
    version='0.0.0b3',
    packages=["csiquant"],
    cmdclass={'build_ext' : build_ext},
    package_data={
        'csiquant' : ['*.pyx', '*.pxd']
    },
    ext_modules=extensions,
)