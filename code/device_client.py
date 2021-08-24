"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT license.

IoT device client class for connecting to Azure IoT Central
as an IoT device, receiving commands and sending telemetry
"""

import os

from dotenv import load_dotenv

from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodRequest, MethodResponse

class DeviceClient:
    """IoT device client class for connecting to Azure IoT Central
    as an IoT device, receiving commands and sending telemetry
    """
    def __init__(self):
        # Load the connection details from IoT Central for the device
        load_dotenv()
        self.__id_scope = os.environ['ID_SCOPE']
        self.__device_id = os.environ['DEVICE_ID']
        self.__primary_key = os.environ['PRIMARY_KEY']

        self.__device_client = None
        self.__on_command = None

    async def __method_request_handler(self, method_request: MethodRequest) -> None:
        print('Command received:', method_request.name)

        if self.__on_command is not None:
            status = await self.__on_command(method_request.name)
        else:
            status = 404

        # Send a response - all commands need a response
        method_response = MethodResponse.create_from_method_request(method_request, status, {})
        await self.__device_client.send_method_response(method_response)

    async def connect_device(self) -> None:
        """Connects this device to IoT Central
        """
        # Connect to the device provisioning service and request the connection details
        # for the device
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host='global.azure-devices-provisioning.net',
            registration_id=self.__device_id,
            id_scope=self.__id_scope,
            symmetric_key=self.__primary_key)
        registration_result = await provisioning_device_client.register()

        # Build the connection string - this is used to connect to IoT Central
        conn_str = 'HostName=' + registration_result.registration_state.assigned_hub + \
                    ';DeviceId=' + self.__device_id + \
                    ';SharedAccessKey=' + self.__primary_key

        # The device client object is used to interact with Azure IoT Central.
        self.__device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        # Connect the device client
        print('Connecting')
        await self.__device_client.connect()
        print('Connected')

        # Connect the command handler
        self.__device_client.on_method_request_received = self.__method_request_handler

    @property
    def on_command(self):
        """A callback for when a command is received
        :return: The callback to call
        """
        return self.__on_command

    @on_command.setter
    def on_command(self, value):
        """A callback for when a command is received
        :value: Required. The callback to call
        """
        self.__on_command = value

    async def send_message(self, message: str) -> None:
        """Sends a telemetry message to IoT Central
        :param message: Required. The telemetry to send
        :type message: str
        """
        await self.__device_client.send_message(message)
