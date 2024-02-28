import requests
import json

BASE_URL = 'https://api.meraki.com/api/v1'
headers = { 'X-Cisco-Meraki-API-Key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0' }
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

    if len(networks) > 0:
        print(f'Printing networks for organization {organization["name"]}')
        for network in networks:
            print(f'\tID: {network["id"]}, Name: {network["name"]}, Timezone: {network["timeZone"]}')
    else:
        print(f'There are no networks assigned to organization {organization["name"]}')