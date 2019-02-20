#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PAM Face

Copyright 2017 Philipp Meisberger <team@pm-codeworks.de>
All rights reserved.
"""

from setuptools import setup

import sys
sys.path.insert(0, './src/')

import pamface

setup(
    name            = 'libpam-face',
    version         = pamface.__version__,
    description     = 'Linux Pluggable Authentication Module (PAM) for face authentication',
    author          = 'Philipp Meisberger',
    author_email    = 'team@pm-codeworks.de',
    url             = 'http://www.pm-codeworks.de/pamface.html',
    license         = 'D-FSL',
    package_dir     = {'': 'src'},
    packages        = ['pamface'],
)
