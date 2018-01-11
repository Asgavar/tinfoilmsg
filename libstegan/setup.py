#! /usr/bin/env python3

from setuptools import setup

setup(
    name='libstegan',
    version='0.1',
    py_modules=['libstegan'],
    provides=['libstegan'],
    requires=['Pillow'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    author='Artur Juraszek',
    author_email='asgavar@gmail.com',
    url='https://github.com/Asgavar/tinfoilmsg',
)
