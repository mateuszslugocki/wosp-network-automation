import requests
import json

BASE_URL = 'https://api.meraki.com/api/v1'
headers = {'X-Cisco-Meraki-API-Key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'}
RESOURCE = '/organizations'

call_response = requests.get(BASE_URL + RESOURCE, headers=headers)
try:
    call_response.raise_for_status()
except requests.HTTPError:
    print(f'Failed to get organizations')
    exit(1)
organizations = json.loads(call_response.text)

for organization in organizations:
    RESOURCE = f'/organizations/{organization["id"]}/networks'
    call_response = requests.get(BASE_URL + RESOURCE, headers=headers)
    try:
        call_response.raise_for_status()
    except requests.HTTPError:
        print(f'Failed to get networks from {organization["name"]}')
        continue
    networks = json.loads(call_response.text)

    for network in networks:
        RESOURCE = f'/networks/{network["id"]}/devices'
        call_response = requests.get(BASE_URL + RESOURCE, headers=headers)
        try:
            call_response.raise_for_status()
        except requests.HTTPError:
            print(f'Failed to get devices for {network["name"]}')
            continue
        devices = json.loads(call_response.text)

        if len(devices) > 0:
            print(f'Devices assigned to network {network["name"]}')

            for device in devices:
                if 'name' in device:
                    print(f'\tName: {device["name"]}, Model: {device["model"]}, Serial: {device["serial"]}')
                else:
                    print(f'\tModel: {device["model"]}, Serial: {device["serial"]}')
        else:
            print(f'There are no devices assigned to the network {network["name"]}')
