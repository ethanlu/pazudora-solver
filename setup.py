#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="pazudorasolver",
    version="0.2.2",
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment :: Puzzle Games'
    ],
    packages=find_packages(),
    dependency_links=[],
    install_requires=[
        "termcolor==1.1"
    ],
    tests_require=[],
    cmdclass={}
)
