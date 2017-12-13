version = '0.0.1'

from setuptools import setup

setup(
    name = 'storified',
    version = version,
    url = 'http://github.com/docnow/storified',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['storified.py',],
    scripts = 'storified.py',
    install_requires = ['requests'],
    description = 'Download your Storify data',
)
