'''
Author: Philippe Fremy
License: Gnu GPL (see fname LICENSE)
'''

from src.kl_enum import VERSION

from setuptools import setup

import os, re

# strip out build status
LONG_DESC = ''.join( open('README.md').readlines()[1:] )

print( 'Packaging klotski version: "%s"' % VERSION )

setup(
    name = 'Klotski',
    version = VERSION,
    description = 'A brain-teaser game',
    long_description = LONG_DESC,
    long_description_content_type="text/markdown",
    author = 'Philippe Fremy',
    author_email = 'phil.fremy@free.fr',
    url = 'https://github.com/bluebird75/klotski',
    license = 'GNU GPL',

    project_urls={
        'Source': 'https://github.com/bluebird75/klotski/',
        'Tracker': 'https://github.com/bluebird75/klotski/issues',
    },

    python_requires='>=3.5',
    install_requires=['PyQt5 >= 5.6', 'sip >= 4.18'],
    packages=['klotski'],
    package_dir={'klotski': 'src'},
    package_data = {
        'klotski': [ 'boards.kts', 'klotski-icon.png', 'klotski-tiles.png', 'README.md' ],
    },

    entry_points={
        'gui_scripts': [
            'klotski=klotski.klotski:main',
        ],
    },

    keywords = 'game',
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        # GNU GPL v2 or above
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',

        # Runs on Windows, unix and MacOs
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',

        # This version is for python 3 only
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',

        'Topic :: Education',
        'Topic :: Games/Entertainment :: Board Games',

        # Indicate who your project is intended for
        'Intended Audience :: Education',

        'Natural Language :: English',
    ],

)




