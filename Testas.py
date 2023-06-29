import requests
from teltonika_auth import authenticate

# Usage example
router_ip = '192.168.1.1'  # Replace with your router's IP address
username = 'admin'  # Replace with your router's username
password = 'Admin123'  # Replace with your router's password

access_token = authenticate(router_ip, username, password)
if access_token:
    # Use the access token to make subsequent API requests
    # For example, you can print the router's device information
    info_url = f"http://{router_ip}/api/device/info"
    headers = {'Authorization': f'Bearer {access_token}'}
    print(headers)
    response = requests.get(info_url, headers=headers)
    if response.status_code == 200:
        device_info = response.json()
        print("Device Information:")
        print(device_info)
    else:
        print("Failed to retrieve device information.")