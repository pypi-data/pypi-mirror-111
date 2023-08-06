"""
Copyright 2021 Charles McMarrow
"""

# built-in
from distutils.core import setup
import os

with open(os.path.join("README.rst")) as readme:
    long_description = readme.read()

setup(
    name="backrooms",
    version="0.2.0",
    author="Charles McMarrow",
    author_email="Charles.McMarrow.4@gmail.com",
    url="https://github.com/cmcmarrow/backrooms",
    license="Apache Software License 2.0",
    description="3D, CISC Architecture and Esolang",
    description_content_type="text/plain",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=["backrooms",
              "backrooms.backrooms_builtins"],

    extras_require={"dev": ["wheel", "check-manifest", "twine", "pyinstaller"]},

    classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Natural Language :: English",
                 "Operating System :: Microsoft :: Windows",
                 "Operating System :: POSIX :: Linux",
                 "Operating System :: MacOS :: MacOS X",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9"],

    entry_points={"console_scripts": ["backrooms = backrooms.backrooms:backrooms"]}
)
