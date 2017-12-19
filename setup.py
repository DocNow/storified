version = '0.0.8'

from setuptools import setup

setup(
    name = 'storified',
    version = version,
    url = 'http://github.com/docnow/storified',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    py_modules = ['storified',],
    scripts = ['storified.py',],
    install_requires = ['requests', 'beautifulsoup4', 'six'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    description = 'Download your Storify data',
)
