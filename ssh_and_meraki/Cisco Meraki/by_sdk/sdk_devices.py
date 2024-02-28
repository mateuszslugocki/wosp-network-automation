import meraki

API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

meraki = meraki.DashboardAPI(API_KEY)

organizations = meraki.organizations.getOrganizations()

for organization in organizations:
    collect = {
        'organization_id': organization['id'],
    }

    try:
        networks = meraki.organizations.getOrganizationNetworks(organization['id'])
    except Exception:
        print(f"Failed to get organization {organization['name']} networks")
        continue

    if len(networks) > 0:
        for network in networks:
            devices = meraki.networks.getNetworkDevices(network['id'])
            if devices:
                print('Devices assigned to network {name}:'.format(name=network['name']))
            else:
                print('There are no devices assigned to the network {network}'.format(network=network['name']))
                continue

            for device in devices:
                    if 'name' in device:
                        print('\tName: {name}, Model: {model}, Serial: {serial}'.format(name=device['name'],
                                                                                        model=device['model'],
                                                                                        serial=device['serial']))
                    else:
                        print('\tModel: {model}, Serial: {serial}'.format(model=device['model'],
                                                                        serial=device['serial']))
