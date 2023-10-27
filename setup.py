#!/usr/bin/env python3
# coding: UTF-8

from setuptools import setup

setup(
    name='dummy',
    version='0.1.1',
    description='Create a dummy file for testing.',
    author='Taichi Kotake',
    packages=['dummy'],
    entry_points={
        'console_scripts': [
            'dummy=dummy.cli:parse_args'
        ]
    },
    install_requires=[
        'colorama',
        'Pillow',
        'reportlab'
    ],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ],
)