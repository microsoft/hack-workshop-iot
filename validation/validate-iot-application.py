import asyncio
import json
import requests

from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodRequest, MethodResponse

print('IoT application validation')

# Ask for the API token and URL
print('What is your IoT application API token?')
api_token = input().strip()

print('What is your application URL?')
url = input().strip()

# Get all the devices
headers = {
    'Authorization': api_token
}

url = url.lower().replace('https://', '')
url = url.split('/')[0]
if url.find('.azureiotcentral.com') == -1:
    url += '.azureiotcentral.com'

devices_url = f'https://{url}/api/devices?api-version=1.0'

response = requests.get(devices_url, headers=headers)

# Get the first device
device_id = response.json()['value'][0]['id']

# Get the device credentials
device_credentials_url = f'https://{url}/api/devices/{device_id}/credentials?api-version=1.0'
response = requests.get(device_credentials_url, headers=headers)

id_scope = response.json()['idScope']
primary_key = response.json()['symmetricKey']['primaryKey']

command_executed = False

async def main():
    global command_executed
    # Pretend to be the device and provision a connection
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host='global.azure-devices-provisioning.net',
        registration_id=device_id,
        id_scope=id_scope,
        symmetric_key=primary_key)
    registration_result = await provisioning_device_client.register()

    # Build the connection string - this is used to connect to IoT Central
    conn_str='HostName=' + registration_result.registration_state.assigned_hub + \
                ';DeviceId=' + device_id + \
                ';SharedAccessKey=' + primary_key

    # The device client object is used to interact with Azure IoT Central.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client
    print(f'Connecting as device {device_id}')
    await device_client.connect()
    print('Connected')

    async def method_request_handler(method_request: MethodRequest) -> None:
        print('Command received:', method_request.name)
            
        # Send the breed to IoT Central
        telemetry = {'Breed': 'american-staffordshire-terrier'}
        await device_client.send_message(json.dumps(telemetry))

        # Send a response - all commands need a response
        method_response = MethodResponse.create_from_method_request(method_request, 200, {})
        await device_client.send_method_response(method_response)

        global command_executed
        command_executed = True

    device_client.on_method_request_received = method_request_handler

    # Execute the command
    command_url = f'https://{url}/api/devices/{device_id}/commands/DetectBreed?api-version=1.0'
    requests.post(command_url, headers=headers, json={})

    time = 0
    while not command_executed and time < 30:
        await asyncio.sleep(1)
        time += 1
    
    # Check that the command was executed
    if not command_executed:
        print('Validation failed - unable to execute Detect Breed command')
        exit(1)
    
    # Get the last breed
    telemetry_url = f'https://{url}/api/devices/{device_id}/telemetry/Breed?api-version=1.0'
    response = requests.get(telemetry_url, headers=headers)

    telemetry_value = response.json()['value']
    print(f'Last detected breed: {telemetry_value}')
    if telemetry_value != 'american-staffordshire-terrier':
        print(f'Validation failed - unable to read back the expected telemetry. Value received was {telemetry_value}')
        exit(1)

    # Disconnect the client
    await device_client.disconnect()

    print('Validation passed!')


# Start the app running
asyncio.run(main())