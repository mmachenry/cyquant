from setuptools import setup
from setuptools.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

package_name = 'csiquant'
def make_sources(*module_names):
    file_type = '.pyx' if use_cython else ".cpp"
    return {
        package_name + '.' + module_name : package_name + "/" + module_name + file_type
        for module_name in module_names
    }

sources = make_sources('dimensions', 'quantities')

extensions = [
    Extension(
        module_name,
        sources=[source],
        language='c++',
        include_dirs=["csiquant/"],
        libraries=[]
    )
    for module_name, source in sources.items()
]


CMDCLASS = {}
if use_cython:
    CMDCLASS.update({'build_ext' : build_ext})

INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {
    "tests" : ["coverage", "pytest"]
}



setup(
    name='csiquant',
    version='0.0.0b3',
    packages=["csiquant"],
    cmdclass=CMDCLASS,
    extras_require=EXTRAS_REQUIRE,
    ext_modules=extensions,
    package_data={
        'csiquant': ['*.pyx', '*.pxd', '*.cpp']
    },
    zip_safe=False
)