#!/usr/bin/env python

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTestCommand(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name="pazudorasolver",
    version="0.2.1",
    author="Ethan Fang Lu",
    author_email="fang.lu@gmail.com",
    description="Puzzles and Dragons board solver",
    keywords="pad",
    url="https://github.com/ethanlu/pazudora-solver",
    download_url="https://github.com/ethanlu/pazudora-solver/releases",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment :: Puzzle Games'
    ],
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
        "termcolor==1.1"
    ],
    tests_require=[
        "pytest"
    ],
    cmdclass={
        'test': PyTestCommand
    }
)
