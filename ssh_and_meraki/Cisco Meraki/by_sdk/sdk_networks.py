import meraki

API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

meraki = meraki.DashboardAPI(API_KEY)

organizations = meraki.organizations.getOrganizations()

for organization in organizations:
    print(f"ID: {organization['id']}, Name: {organization['name']}")

    try:
        networks = meraki.organizations.getOrganizationNetworks(organization['id'])
    except Exception:
        print(f"Failed to get organization {organization['name']} networks")
        continue

    if len(networks) > 0:
        print('Printing networks for organization {name}:'.format(name=organization['name']))

        for network in networks:
            print('\tID: {id}, Name: {name}, TimeZone: {timezone}'.format(id=network['id'],
                                                                  name=network['name'],
                                                                  timezone=network['timeZone']))
    else:
        print(f'There are no networks assigned to organization {organization["name"]}')