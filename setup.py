#!/usr/bin/env python
from setuptools import setup, find_packages

from kipptbackup import __version__

setup(
    name='Kippt Backup',
    version=__version__,
    author='Vaidik Kapoor',
    author_email='kapoor.vaidik@gmail.com',
    description='A utility package to backup Kippt clips.',
    install_requires=['requests>=1.1.0'],
    packages=['kipptbackup'],
    entry_points={
        'console_scripts': [
            'kipptbackup = kipptbackup.runner:backup'
        ]
    }
)
