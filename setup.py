#!/usr/bin/env python2

from setuptools import setup, find_packages
import sys

with open('README.rst', 'r') as f:
  long_description=f.read()

version='0.0.1'

setup(
    zip_safe=True,
    name='carbon-amqp',
    version=version,
    description="Use an AMQP server as a bus for GraphiteDB / Carbon",
    long_description=long_description,
    classifiers=[
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Programming Language :: Python :: 3",
      "Topic :: Utilities",
    ],
    keywords='graphite carbon metrics monitoring amqp',
    author='John Casey',
    author_email='jdcasey@commonjava.org',
    url='https://github.com/jdcasey/carbon-amqp',
    license='GPLv3+',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=[
      "pika",
      "click",
      "ruamel.yaml"
    ],
    test_suite="tests",
)

