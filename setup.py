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
    name="pazudora_solver",
    version="0.1.0",
    author="Ethan Fang Lu",
    author_email="fang.lu@gmail.com",
    description="Puzzles and Dragons board solver",
    keywords="pad",
    url="https://github.com/ethanlu/pazudora-solver",
    download_url="",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Puzzle Games'
    ],
    packages=find_packages("pazudora_solver.*"),
    dependency_links=[],
    install_requires=[
        "pytest==2.8.7",
        "termcolor==1.1"
    ],
    tests_require=[
        "flake8",
        "pytest"
    ],
    cmdclass={
        'test': PyTestCommand
    }
)
