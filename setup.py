#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="pazudora_solver",
    version="0.3",
    author="Ethan Lu",
    author_email="fang.lu@gmail.com",
    description="Puzzles and Dragons board solver",
    keywords="pad",
    url="https://github.com/ethanlu/pazudora-solver",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Puzzle Games'
    ],
    dependency_links=[],
    install_requires=[
        "pytest",
        "termcolor"
    ]
)
