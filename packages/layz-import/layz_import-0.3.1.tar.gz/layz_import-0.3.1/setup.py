#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md', 'rb') as infile:
    readme = infile.read().decode('UTF-8')

tests_require = ['pytest', 'pytest-xdist']

setup(name='layz_import',
      version="0.3.1",
      description='A module for layz loading of Python modules',
      long_description=readme,
      url='https://gitlab.com/caosuna/layz-import',
      author='Carlos Osuna',
      author_email='charlie@caosuna.com',
      license='GNU GPLv3',
      platforms = ["any"],
      classifiers=['Development Status :: 4 - Beta',
                   # Indicate who your project is intended for
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries :: '
                     'Python Modules',

                   'License :: OSI Approved :: '
                     'GNU General Public License v3 or later (GPLv3+)',

                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',

                   'Operating System :: OS Independent',
                   ],
      packages=".",
      install_requires=['six'],
      test_suite='layz_import.test_layz',
      tests_require=tests_require,
      extras_require={'test': tests_require},
      package_data={'layz_import': ['VERSION']}
      )
