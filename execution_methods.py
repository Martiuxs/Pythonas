import requests

def authenticate(router_ip, username, password):
    auth_url = f"http://{router_ip}/api/login"
    response = requests.post(auth_url, json={"username": username, "password": password})
    
    if response.status_code == 200:
        access_token = response.json().get('ubus_rpc_session')
        print("Authentication successful!")
        return access_token
    else:
        print("Authentication failed.")
        return None

router_ip = '192.168.1.1'
username = 'admin' 
password = 'Admin123' 
phone_number = '+37063032518'  
message = 'Wi-Fi configuration change detected!' 

def send_sms_not(router_ip, access_token, phone_number, message):
    sms_url = f"http://{router_ip}/api/services/mobile_utilities/sms_rules/config"
    headers = {'Authorization': f'Bearer {access_token}'}

    payload = {
        "phone_number": phone_number,
        "message": message
    }

    response = requests.post(sms_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("SMS sent successfully!")
    else:
        print("Failed to send SMS.")




access_token = authenticate(router_ip, username, password)
if access_token:
    info_url = f"http://{router_ip}/api/services/mobile_utilities/sms_rules/config"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(info_url, headers=headers)
    if response.status_code == 200:
        device_info = response.json()
        print("Device Information:")
        print(device_info)
    else:
        print("Failed to retrieve device information.")

