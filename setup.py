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
                      'PIL'
    ],
    # entry_points = {"console_scripts": [
    #       'ad_relink = astro_data_store.astro_data_store:relink',
    #       'ad_project = astro_data_store.astro_data_store:project',
    #       'ad_require = astro_data_store.astro_data_store:require',
    #       'ad_legacy = astro_data_store.astro_data_store:move_legacy'
    #         ]
    #                   },
)
