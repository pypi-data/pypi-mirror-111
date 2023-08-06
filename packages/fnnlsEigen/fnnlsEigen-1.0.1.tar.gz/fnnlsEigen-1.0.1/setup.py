from setuptools import find_packages, setup, Extension

import numpy as np
import os
import sys


with open("README.md", "r") as f:
    long_description = f.read()


def get_eigen_include():
    EIGEN = "thirdparty/eigen"
    DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(DIRECTORY, EIGEN)
    return [path]


def get_extra_compile_args():
    if sys.platform == "linux" or sys.platform == "linux2":
        extra_compile_args = [
            '--std=c++14',
            '-fPIC',
            '-Wall',
            '-Werror',
            '-pedantic',
            # '-Wshadow', # Cython creates its own shadow mess
            '-Wextra',
            '-faligned-new',
            '-O3',
            # '-march=native', # Building for specific arch makes it 30 % faster on amd but 100 % slower on intel
            '-DNDEBUG',
            '-DEIGEN_NO_DEBUG',
            '-funroll-loops',
            '-fomit-frame-pointer',
        ]
    elif sys.platform == "darwin":
        raise OSError('MAC OS X is not yet supported')
    elif sys.platform == "win32":
        extra_compile_args = [
            '/std:c++14',
            '/Ox',
            '/Qfast_transcendentals',
            '/Oy',
            '/GA',
            '/DNDEBUG',
            '/DEIGEN_NO_DEBUG',
        ]
    else:
        raise OSError('Unsupported OS')
    return extra_compile_args


extension = Extension(name='fnnlsEigen',
                      sources=['fnnlsEigen/eigen_fnnls.pyx'],
                      language='c++',
                      include_dirs=[np.get_include()] + get_eigen_include(),
                      extra_compile_args=get_extra_compile_args(),
                      define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
                      )


setup(
    name="fnnlsEigen",
    version="1.0.1",
    packages=find_packages(),
    author="Mikael Twengström",
    author_email="m.twengstrom@gmail.com",
    description="A fast nnls solver for python implemented in C++ using Eigen",
    long_description=long_description,
    license="MIT",
    platforms=["Linux", "Windows"],
    long_description_content_type='text/markdown',
    url="https://github.com/mikaeltw/fnnlsEigen",
    ext_modules=[extension],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    install_requires=[
        'numpy>=1.20.2',
        'Cython>=0.29.23',
    ],
    python_requires=">=3.7.8",
)
