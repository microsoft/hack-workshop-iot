# Goal 3: Deploy device code

Your team has trained an ML model and set up an IoT application. The final task for your team is to deploy code to your Raspberry Pi and test out your application.

> 💻 If you are using a PC or Mac instead of a Pi, your team can run the code locally.

## The code

The code has been provided for you in the [code](./code) folder, so make sure you clone this repo. This code is Python code that will connect to your IoT Central application and wait for the *Detect Breed* command. Once this command is received, it will take a picture using either the Raspberry Pi Camera module, or a USB web cam. The detected breed will be sent back to the IoT Central application and you will be able to see it on the dashboard.

The code has the following files:

| File                     | Description                                                                                                                 |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| .env                     | This file contains configuration for the app                                                                                |
| app.py                   | This file contains the core application logic                                                                               |
| camera.py                | This file contains the `Camera` class that interacts with the Raspberry Pi Camera module or USB web cam to capture images   |
| classifier.py            | This file contains the `Classifier` class that uses the Custom Vision image classifier to classify an image from the camera |
| device_client.py         | This file contains the `DeviceClient` class that connects to IoT Central, listens for commands and sends telemetry          |
| requirements.txt         | This file contains the Pip packages that are needed to run this code on a Raspberry Pi                                      |
| requirements-linux.tx  t | This file contains the Pip packages that are needed to run this code on Linux                                               |
| requirements-macos.txt   | This file contains the Pip packages that are needed to run this code on macOS                                               |
| requirements-windows.txt | This file contains the Pip packages that are needed to run this code on Windows                                             |

Take some time to read this code and understand what it does, particularly the `device_client.py` and `classifier.py` files. These use the `azure-iot-device` abd `azure-cognitiveservices-vision-customvision` Pip packages respectively to work with the various cloud services.

The configuration for the code is in the `.env` file. You will need to set the following values:

| Value          | Description                                                                                           |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| ID_SCOPE       | The value of the ID Scope from the connection dialog for your `mutt-matcher` device in IoT Central    |
| DEVICE_ID      | The value of the device ID from the connection dialog for your `mutt-matcher` device in IoT Central   |
| PRIMARY_KEY    | The value of the primary key from the connection dialog for your `mutt-matcher` device in IoT Central |
| CAMERA_TYPE    | Set this to PiCamera if you are using the Raspberry Pi Camera module, otherwise set it to USB         |
| PREDICTION_URL | The prediction URL for your published model iteration from Custom Vision                              |
| PREDICTION_KEY | The prediction key for your published model iteration from Custom Vision                              |

You will need to install the Pip packages from one of the `requirements.txt` files:

```sh
pip3 install -r requirements.txt
```

- If you are using a Raspberry Pi, use `requirements.txt`
- If you are using Linux, use `requirements-linux.txt`
- If you are using macOS, use `requirements-macos.txt`
- If you are using Windows, use `requirements-windows.txt`

This code needs to be run with Python 3. Raspberry Pi's come with Python 2 as well as Python 3.

```sh
python3 app.py
```

> 💻 If you are using a PC or Mac instead of a Pi, you should [set up a virtual environment](https://docs.python.org/3/library/venv.html) and install the Pip packages inside that, as well as running code from the activated virtual environment.

## Success criteria

Your team will work together to deploy this code on your Mutt Matcher device. Your team will have achieved this goal when the following success criteria is met:

- All the code has been copied to the device.
- The `.env` file has been updated with the relevant values.
- Your code is running, and able to take a picture and detect a breed, seeing the results in you IoT Central app.

## Validation

Have a mentor check your device. They should be able to point the device at an one of the training images loaded on a screen, select the *Detect Breed* button, then see the correct result in the IoT Central application.

## Tips

- You can copy code onto your device using VS Code. Connect to the Pi using the VS Code remote SSH extension, open a folder on your Pi, then drag the code into the VS Code explorer from your File Explorer or Finder. You will need all 3 files in the [code](./code) folder.

- If you are using the Raspberry Pi camera module, the code assumes you have this cable side up. If you want to have the camera cable side down, or sideways, you need to change the value of `CAMERA_ROTATION` in `camera.py` to the right value. `0` means the cable is at the bottom, `90` for the cable on one side, `270` for the cable on the other side.

- If you are using a USB web cam, the `CAMERA_INDEX` value in `camera.py` defines which camera is used. If you only have 1 camera attached, this should be 0. If you have multiple, you can change this value.

- You can validate the images taken from the Custom Vision portal. When images are classified, they appear in the *Predictions* tab in Custom Vision. You can use this to validate your camera is configured correctly.

- Unless you have a dog of the relevant breed handy, you can test the app out by loading one of the pictures from the [model-images/testing-images](./model-images/testing-images) and having that on your screen, then pointing the camera on the Mutt Matcher at your screen.

- The `requirements-macos.txt` file has been tested on an M1 mac running macOS Big Sur 11.5.2. If you have any issues on other configurations, you may need to change the versions of the Pip packages installed.

- The `requirements-windows.txt` file has been tested on a Intel PC running Windows 10 21H1. If you have any issues on other configurations, you may need to change the versions of the Pip packages installed.

## Final result

Once your code is running, you should have a complete IoT application!
