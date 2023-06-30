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