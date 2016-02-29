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
    version="0.1.3",
    author="Ethan Fang Lu",
    author_email="fang.lu@gmail.com",
    description="Puzzles and Dragons board solver",
    keywords="pad",
    url="https://github.com/ethanlu/pazudora-solver",
    download_url="https://github.com/ethanlu/pazudora-solver/releases/tag/0.1.3",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Puzzle Games'
    ],
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
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
