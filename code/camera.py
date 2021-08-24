"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT license.

Camera class for capturing images from a Raspberry Pi Camera module, or a USB web cam
"""

from io import BytesIO
import os
import time

from dotenv import load_dotenv

# Allow PiCamera to fail as local versions won't have a camera
try:
    from picamera import PiCamera
except:
    pass

import cv2

CAMERA_ROTATION = 180
CAMERA_INDEX = 0

# pylint: disable=too-few-public-methods,no-member
class Camera:
    """Camera class for capturing images from a Raspberry Pi Camera module, or a USB web cam
    """
    def __init__(self):
        # Load the camera settings
        load_dotenv()
        self.__camera_type = os.environ['CAMERA_TYPE']

        # pylint: disable=no-else-return
        if self.__camera_type.lower() == 'picamera':
            self.__camera = PiCamera()
            self.__camera.resolution = (640, 480)
            self.__camera.rotation = CAMERA_ROTATION
            time.sleep(2)
        else:
            self.__camera = cv2.VideoCapture(CAMERA_INDEX)

    # Take a picture
    def take_picture(self) -> BytesIO:
        """Takes a picture from a Raspberry Pi Camera module, or a USB web cam
        :return: The image as a byte stream
        :rtype: BytesIO
        """
        # pylint: disable=no-else-return
        if self.__camera_type.lower() == 'picamera':
            # If we are using the PiCamera, capture a jpeg directly into a BytesIO object
            image = BytesIO()
            self.__camera.capture(image, 'jpeg')
            # Rewind the BytesIO and return it
            image.seek(0)
            return image
        else:
            # If we are using a USB webcam, capture an image using OpenCV
            _, image = self.__camera.read()
            # Encode the image as a JPEG into a byte buffer
            _, buffer = cv2.imencode('.jpg', image)
            # Copy the byte buffer into a BytesIO object and retturn it
            return BytesIO(buffer)
