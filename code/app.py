"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT license.

Main application code for the Mutt Matcher hackathon workshop
"""

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import asyncio
import json

from camera import Camera
from classifier import Classifier
from device_client import DeviceClient

CAMERA = Camera()
CLASSIFIER = Classifier()
DEVICE_CLIENT = DeviceClient()

# The main app loop that keeps the app alive
async def main() -> None:
    """The main loop
    """
    # Connect the IoT device client
    await DEVICE_CLIENT.connect_device()

    # Define a callback that is called when a command is received from IoT Central
    async def command_handler(command_name: str) -> int:
        # Define a return status - 404 for not found unless the command name is one we know about
        status = 404

        # If the detect breed command is invoked, use the camera to detect the breed
        if command_name == 'DetectBreed':
            status = 200

            # Take a picture
            image = CAMERA.take_picture()

            # Get the highest predted breed from the picture
            breed = CLASSIFIER.classify_image(image)

            print('Breed detected:', breed)

            # Send the breed to IoT Central
            telemetry = {'Breed': breed}
            await DEVICE_CLIENT.send_message(json.dumps(telemetry))

        return status

    # Connect the command handler
    DEVICE_CLIENT.on_command = command_handler

    # Loop forever
    while True:
        await asyncio.sleep(60)

# Start the app running
asyncio.run(main())
