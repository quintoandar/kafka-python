#!/usr/bin/env python
import sys
from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

if sys.version_info < (3, 5):
    raise Exception("Only Python 3.5+ is supported")

raw_requirements = parse_requirements("requirements.txt", session=False)
requirements = [str(ir.req) for ir in raw_requirements]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="quintoandar_kafka",
    version="2.0.0",
    author="QuintoAndar",
    author_email="rodrigo.oliveira@quintoandar.com.br",
    description="Checks messages to avoid reprocessing events.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quintoandar/kafka-python",
    packages=find_packages(exclude=["ez_setup", "examples", "tests", "release"]),
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
