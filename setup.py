# Copyright (C) 2015-2016, Christof Buchbender
r"""
"""

from setuptools import setup


setup(
    name='copy_sd_card',
    version=open('VERSION').read().strip(),
    author='Christof Buchbender',
    author_email='buchbend@ph1.uni-koeln.de',
    packages=['copy_sd_card'],
    license='LICENSE.txt',
    description=('TBD'),
    long_description=open('README.md').read(),
    install_requires=['generaltools',
    ],
    entry_points = {"console_scripts": [
          'monitor_inbox = copy_sd_card.monitor_inbox:main'
            ]
                      },
)
