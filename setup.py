import os
from setuptools import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name="graphs",
    version="0.1.0",
    author="Sumeet Gyanchandani",
    author_email="sumeet.gyanchandani@gmail.com",
    description=("An demonstration of how to an graph object from a list of edges"),
    license="MIT",
    keywords="graphs",
    url="https://packages.python.org/graphs_demo",
    packages=['lib', 'tests', 'test_data'],
    long_description=read('README.md'),
    install_requires=[
        'numpy==1.23.5',
        'matplotlib==3.6.2',
        'pytest==7.1.2'
    ],
)
