"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT license.

Classifier class for sending images to a Custom Vision image classifier and getting the top
prediction
"""

from io import BytesIO
import os

from dotenv import load_dotenv
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# pylint: disable=too-few-public-methods
class Classifier:
    """Classifier class for sending images to a Custom Vision image classifier and getting
    the top prediction
    """
    def __init__(self):
        # Load the custom vision settings
        load_dotenv()
        prediction_url = os.environ['PREDICTION_URL']
        prediction_key = os.environ['PREDICTION_KEY']

        # Decompose the prediction URL
        parts = prediction_url.split('/')
        endpoint = 'https://' + parts[2]
        self.__project_id = parts[6]
        self.__iteration_name = parts[9]

        # Create the image classifier predictor
        prediction_credentials = ApiKeyCredentials(in_headers={'Prediction-key': prediction_key})
        self.__predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)

    def classify_image(self, image: BytesIO) -> str:
        """Classifies an image and returns the tag with the highest probability
        :param image: Required. The image to classify
        :type image: BytesIO
        :return: The tag for the highest prediction
        :rtype: str
        """
        # Send the image to the classifier to get the predictions
        results = self.__predictor.classify_image(self.__project_id, self.__iteration_name, image)

        # The predictions come in order of probability, so the first is the best
        best_prediction = results.predictions[0]

        # print the predictions and find the one with the highest probability
        print('Predictions:')
        for prediction in results.predictions:
            print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%')

        return best_prediction.tag_name
