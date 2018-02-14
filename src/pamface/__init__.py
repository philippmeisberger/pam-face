#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PAM Face

Copyright 2018 Philipp Meisberger <team@pm-codeworks.de>
All rights reserved.
"""

import cv2

__version__ = '1.0'
CONFIG_FILE = '/etc/pamface/pamface.conf'
MODELS_FILE = '/etc/pamface/models.xml'
FACE_CASCADE_FILE = '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml'

def createLBPHFaceRecognizer():
    ## OpenCV 3 installed?
    if (int(cv2.__version__[0]) >= 3):
        return cv2.face.createLBPHFaceRecognizer()
    else:
        return cv2.createLBPHFaceRecognizer()
