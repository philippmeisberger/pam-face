#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PAM Face

Copyright 2018 Philipp Meisberger <team@pm-codeworks.de>
All rights reserved.
"""

import cv2
import numpy
import os

from pamface import MODELS_FILE

def checkOpenCVVersion(major, minor = 0):
    """
    Checks for a given OpenCV version.

    @param major The major version
    @þaram minor The minor version
    @return boolean
    """

    return ((int(cv2.__version__[0]) >= major) and (int(cv2.__version__[2]) >= minor))

class PamFaceRecognizer(object):
    """
    Wrapper around OpenCV FaceRecognizer to support OpenCV 2 and 3.

    OpenCV FaceRecognizer instance
    @var FaceRecognizer __faceRecognizer

    OpenCV VideoCapture instance
    @var VideoCapture __videoCapture

    OpenCV FaceCascade instance
    @var FaceCascade __faceCascade
    """

    __faceRecognizer = None
    __videoCapture = None
    __faceCascade = None

    def __init__(self, camera):
        """
        Constructor for creating a PamFaceRecognizer instance.

        @param camera Camera device e.g. -1 is default device.
        """

        try:
            camera = int(camera)

        except ValueError:
            ## camera is path
            pass

        self.__videoCapture = cv2.VideoCapture(camera)
        self.__faceCascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

        ## Initialize FaceRecognizer
        if (checkOpenCVVersion(3, 3)):
            self.__faceRecognizer = cv2.LBPHFaceRecognizer_create()
        elif (checkOpenCVVersion(3)):
            self.__faceRecognizer = cv2.face.createLBPHFaceRecognizer()
        else:
            self.__faceRecognizer = cv2.createLBPHFaceRecognizer()

        ## Check if models.xml is readable
        if (os.access(MODELS_FILE, os.R_OK) == False):
            raise Exception('The models file "' + MODELS_FILE + '" is not readable!')

        ## Any model trained?
        if (os.path.getsize(MODELS_FILE) > 0):
            if (checkOpenCVVersion(3, 3)):
                self.__faceRecognizer.read(MODELS_FILE)
            else:
                self.__faceRecognizer.load(MODELS_FILE)

    def __del__(self):
        """
        Destructor for destroying a PamFaceRecognizer instance.

        """

        if (self.__videoCapture != None):
            self.__videoCapture.release()

    def detectFaces(self):
        """
        Detects all faces in front of video device.

        @return Image areas as rectangles and gray-scale image
        """

        result, image = self.__videoCapture.read()
        grayScaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return (self.__faceCascade.detectMultiScale(grayScaleImage, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE), grayScaleImage)

    def predict(self, image):
        """
        Tries to predict a user on a specified image.

        @param image Image of user.
        @return tuple
        """

        return self.__faceRecognizer.predict(image)

    def update(self, faces, labels):
        """
        Updates face model of a specified user.

        @param faces Face images
        @param labels Usernames
        """

        self.__faceRecognizer.update(numpy.array(faces), numpy.array(labels))

        ## Store model
        if (checkOpenCVVersion(3, 3)):
            self.__faceRecognizer.write(MODELS_FILE)
        else:
            self.__faceRecognizer.save(MODELS_FILE)
