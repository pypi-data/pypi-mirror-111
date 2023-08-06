# coding=utf-8
from setuptools import setup

setup(
    name = 'magic_flux_led',
    packages = ['magic_flux_led'],
    version = '0.25',
    description = 'A Python library to communicate with the flux_led smart bulbs',
    author = 'Daniel Hjelseth Høyer, modified by Chris Haun',
    author_email = 'chris.r.haun@gmail.com',
    url = 'https://github.com/icemanch/flux_led',
    license = 'LGPLv3+',
    include_package_data = True,
    keywords = [
        'flux_led',
        'smart bulbs',
        'light',
        'magic_flux_led',
        'magic home',
        ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ' +
            'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'magic_flux_led = magic_flux_led.__main__:main'
        ]
    },
)
