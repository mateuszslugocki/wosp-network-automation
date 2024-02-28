import meraki

API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

meraki = meraki.DashboardAPI(API_KEY)

organizations = meraki.organizations.getOrganizations()

for organization in organizations:
    print(f"ID: {organization['id']}, Name: {organization['name']}")
