"""Setup script for infuradj"""

import os.path

from setuptools import find_packages, setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="infuradj",
    version="1.0.3",
    description="Send tx from Django with infura",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dastanbeksamatov/django-infura",
    author="Dastan Samatov",
    author_email="dastanbeksamatov@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(include=['infuradj']),
    include_package_data=True,
    install_requires=[
        "web3==5.20.0"
    ],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=['pytest==4.4.1', "python-decouple==3.4"],
)
