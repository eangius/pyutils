#!usr/bin/env python

import source as proj
import setuptools
import sys


# Common & relative values.
PY_VERSION = sys.version_info
PROJ_LICENSE = 'MIT'


setuptools.setup(
    # Metadata
    name=proj.__name__,
    version=proj.__version__,
    description='',
    url=f'https://github.com/eangius/{proj.__name__}',
    author='Elian Angius',
    license=PROJ_LICENSE,
    packages=[proj.__name__],
    keywords='utilities',

    # Dependencies to auto install.
    python_requires=f'>={PY_VERSION.major}.${PY_VERSION.minor}',
    install_requires=[],
    platforms=["any"],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        f"Programming Language :: Python :: {PY_VERSION.major}",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        f"License :: OSI Approved :: {PROJ_LICENSE} License",
        "Topic :: Library",
    ],
)
