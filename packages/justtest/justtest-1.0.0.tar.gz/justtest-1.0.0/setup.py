# This is a test for pip
from __future__ import absolute_import
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
    name='justtest',
    version='1.0.0',
    description='test',
    author='test',
    packages=find_packages(),
    install_requries=[
        'numpy'
    ],
    python_requires='>=3.7, <4',
    license='Apache 2.0'
)



