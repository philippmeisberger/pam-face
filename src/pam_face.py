#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PAM Face implementation

Copyright 2017 Philipp Meisberger <team@pm-codeworks.de>
All rights reserved.
"""

import syslog
import os
import ConfigParser
import numpy
import cv2

from pamface import __version__ as VERSION
from pamface import CONFIG_FILE
from pamface import MODELS_FILE
from pamface import FACE_CASCADE_FILE

class UserUnknownException(Exception):
    """
    Dummy exception class for unknown user.

    """

    pass

def showPAMTextMessage(pamh, message, errorMessage=False):
    """
    Shows a PAM conversation text info.

    @param pamh
    The PAM handle.

    @param str message
    The message to print.

    @return bool
    """

    try:
        if (errorMessage == True):
            style = pamh.PAM_ERROR_MSG
        else:
            style = pamh.PAM_TEXT_INFO

        msg = pamh.Message(style, 'PAM Face ' + VERSION + ': '+ str(message))
        pamh.conversation(msg)
        return True

    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return False


def auth_log(message, priority=syslog.LOG_INFO):
    """
    Sends errors to default authentication log

    @param str message
    The message to write to syslog.

    @param int priority
    The priority of the syslog message.

    @return void
    """

    syslog.openlog(facility=syslog.LOG_AUTH)
    syslog.syslog(priority, 'PAM Face: ' + message)
    syslog.closelog()


def pam_sm_authenticate(pamh, flags, argv):
    """
    PAM service function for user authentication.

    @param pamh
    @param flags
    @param argv

    @return int
    """

    ## The authentication service should return [PAM_AUTH_ERROR] if the user has a null authentication token
    flags = pamh.PAM_DISALLOW_NULL_AUTHTOK

    ## Initialize authentication progress
    try:
        ## Tries to get user which is asking for permission
        userName = pamh.ruser

        ## Fallback
        if (userName == None):
            userName = pamh.get_user()

        ## Be sure the user is set
        if (userName == None):
            raise UserUnknownException('The user is not known!')

        # Checks if path/file is readable
        if (os.access(CONFIG_FILE, os.R_OK) == False):
            raise Exception('The configuration file "' + CONFIG_FILE + '" is not readable!')

        configParser = ConfigParser.ConfigParser()
        configParser.read(CONFIG_FILE)

        ## Log the user
        auth_log('The user "' + userName + '" is asking for permission for service "' + str(pamh.service) + '".', syslog.LOG_DEBUG)

        ## Checks if the the user was added in configuration
        if (configParser.has_option('Users', userName) == False):
            raise Exception('The user was not added!')

        # Check if models.xml is readable
        if (os.access(MODELS_FILE, os.R_OK) == False):
            raise Exception('The models file "' + MODELS_FILE + '" is not readable!')

        ## Read configuration data
        userLabel = int(configParser.get('Users', userName))
        threshold = int(configParser.get('Authentication', 'Threshold'))

        ## camera can be index or path
        camera = configParser.get('Global', 'Camera')

        try:
            camera = int(camera)

        except ValueError:
            ## camera is path
            pass

        videoCapture = cv2.VideoCapture(camera)
        faceRecognizer = cv2.createLBPHFaceRecognizer()
        faceRecognizer.load(MODELS_FILE)

        ## Authentication progress
        showPAMTextMessage(pamh, 'Recognizing face ...')
        faceCascade = cv2.CascadeClassifier(FACE_CASCADE_FILE)

        ## Try to predict user
        for _ in range(30):
            result, frame = videoCapture.read()
            grayScaleImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = grayScaleImage

            ## Detect face
            faces = faceCascade.detectMultiScale(grayScaleImage, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

            ## Draw a green rectangle around the faces
            for (x, y, w, h) in faces:
                face = grayScaleImage[y:y+h,x:x+w]
                break

            predict = faceRecognizer.predict(face)

            if (predict[1] <= threshold):
                break

        videoCapture.release()

        ## User found?
        if ((predict[0] == userLabel) and (predict[1] <= threshold)):
            auth_log('Access granted!')
            showPAMTextMessage(pamh, 'Access granted!')
            return pamh.PAM_SUCCESS
        else:
            auth_log('Face not recognized!', syslog.LOG_WARNING)
            showPAMTextMessage(pamh, 'Access denied!', True)
            return pamh.PAM_AUTH_ERR

    except UserUnknownException as e:
        auth_log(str(e), syslog.LOG_ERR)
        showPAMTextMessage(pamh, 'Access denied!', True)
        return pamh.PAM_USER_UNKNOWN

    except Exception as e:
        auth_log(str(e), syslog.LOG_ERR)
        return pamh.PAM_IGNORE

    ## Denies for default
    return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
    """
    PAM service function to alter credentials.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
    """
    PAM service function for account management.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
    """
    PAM service function to start session.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    """
    PAM service function to terminate session.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
    """
    PAM service function for authentication token management.

    @param pamh
    @param flags
    @param argv
    @return int
    """

    return pamh.PAM_SUCCESS
