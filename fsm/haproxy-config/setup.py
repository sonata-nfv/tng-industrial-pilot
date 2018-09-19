# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='haproxy configuration',

    version='0.1',

    description='FSM haproxy configuration',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/sonata-nfv/tng-industrial-pilot/fsm/haproxy-config',

    # Author details
    author='Miguel Mesquita',
    author_email='mesquita@alticelabs.com',

    # Choose your license
    license='Apache 2.0',

    # What does your project relate to?
    keywords='NFV orchestrator',

    packages=find_packages("haproxy-config"),
    install_requires=['pytest', 'ansible>=2.4.0.0'],
    setup_requires=['pytest-runner'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': ['fsm-haproxy=tngfsm_css.__main__:main'],
    },
)
