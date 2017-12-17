version = '0.0.5'

from setuptools import setup

setup(
    name = 'storified',
    version = version,
    url = 'http://github.com/docnow/storified',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['storified',],
    scripts = ['storified.py',],
    install_requires = ['requests'],
    description = 'Download your Storify data',
)
