#from distutils.core import setup
from setuptools import find_packages, setup
from Cython.Build import cythonize
import numpy

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="ROA",
    version="1.3",
    packages=find_packages(),
    author="Fergus Donnan",
    description="A simple function to compute the running optimal average and effective no. of parameters.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/FergusDonnan/Running-Optimal-Average",

    ext_modules = cythonize("ROA.pyx", annotate=True,
        compiler_directives={'wraparound': False,
                            'nonecheck': False,
                            'cdivision': True,
                            'boundscheck':False
                            }),
    include_dirs=[numpy.get_include()],
    install_requires=[
        'numpy>=1.19.2']
)

