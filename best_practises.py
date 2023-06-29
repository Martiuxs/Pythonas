import requests

def authenticate_and_get_device_info(router_ip, username, password):
    auth_url = f"http://{router_ip}/api/login"
    response = requests.post(auth_url, json={"username": username, "password": password})

    if response.status_code == 200:
        access_token = response.json().get('data').get('access_token')
        print("Authentication successful!")

        info_url = f"http://{router_ip}/api/device/info"
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(info_url, headers=headers)

        if response.status_code == 200:
            device_info = response.json()
            print("Device Information:")
            print(device_info)
        else:
            print("Failed to retrieve device information.")
    else:
        print("Authentication failed.")

# Usage example
router_ip = '192.168.1.1'  # Replace with your router's IP address
username = 'admin'  # Replace with your router's username
password = 'Admin123'  # Replace with your router's password

authenticate_and_get_device_info(router_ip, username, password)
