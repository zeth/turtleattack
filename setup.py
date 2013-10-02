#!/usr/bin/env python3

"""Setup script for turtle attack."""

from distutils.core import setup

setup(name='turtleattack',
      version='0.1',
      author = "Zeth",
      author_email = "theology@gmail.com",
      url = "https://github.com/zeth/turtleattack",
      license = "MIT",
      keywords = "turtle education kids",
      scripts=['tattack'],
      packages=['turtleattack'],
      package_data={'turtleattack': ['images/*.gif', 'images/fire/*.gif']},
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Simulation",
        ],
      )
