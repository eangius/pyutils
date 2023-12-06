#!usr/bin/env python

import contextlib
import pyutils as proj
import setuptools
from distutils.cmd import Command
import shutil
import sys
import os


# Common & relative values.
PY_VERSION = sys.version_info
PROJ_LICENSE = 'MIT'


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        return

    def finalize_options(self):
        return

    def run(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        for root, dirnames, filenames in os.walk(folder):
            # ignore any hidden folder or file (.venv*, .git*, .dvc*, ...)
            if any(part.startswith(".") for part in root.split(os.path.sep)):
                continue

            # types of build artifacts
            for f in filenames:
                with contextlib.suppress(Exception):
                    if any(f.endswith(file_type) for file_type in {".c", ".so", ".html"}):
                        full_path = os.path.join(root, f)
                        print(f"removing: {full_path}")
                        os.remove(full_path)

            # types of build directories
            for d in dirnames:
                with contextlib.suppress(Exception):
                    if d in {'__pycache__', 'build', 'dist', '.egg-info', '.DS_Store', 'runtime'}:
                        full_path = os.path.join(root, d)
                        print(f"removing: {full_path}")
                        shutil.rmtree(full_path)
        return


setuptools.setup(
    # Metadata
    name=proj.__name__,
    version=proj.__version__,
    description='',
    url=f'https://github.com/eangius/{proj.__name__}',
    author='Elian Angius',
    license=PROJ_LICENSE,
    packages=setuptools.find_packages(
        where='.',
        include=[f'{proj.__name__}*'],
        exclude=['tests'],
    ),
    keywords='utilities',

    # Dependencies to auto install.
    python_requires=f'>={PY_VERSION.major}.{PY_VERSION.minor}',
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

    # custom commands
    cmdclass={
        'clean': CleanCommand,
    },
)
