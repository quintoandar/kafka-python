#!/usr/bin/env python
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 2):
    raise Exception('Only Python 3.2+ is supported')

setup(name='idempotence_client',
      version='0.0.1',
      description="Checks messages to avoid reprocessing events.",
      url='https://github.com/quintoandar/python-kafka-idempotence-client',
      packages=find_packages(exclude=['ez_setup', 'examples',
                                      'tests', 'release']),
      include_package_data=True,
      zip_safe=False)
