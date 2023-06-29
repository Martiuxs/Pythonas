import requests
import json

# Function to authenticate with the router's API
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

# Function to create an event reporting rule for Wi-Fi configuration changes
def create_event_reporting_rule(router_ip, access_token, rule_payload):
    rule_url = f"http://{router_ip}/api/services/events_reporting/config/"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.post(rule_url, headers=headers, json=rule_payload)

    if response.status_code == 201:
        print("Event reporting rule created successfully!")
    else:
        print("Failed to create event reporting rule.")
        
def modify_event_reporting_rule(router_ip, access_token, rule_id, modify_payload):
    rule_url = f"http://{router_ip}/api/services/events_reporting/config/{rule_id}"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.put(rule_url, headers=headers, json=modify_payload)

    if response.status_code == 200:
        print("Event reporting rule modified successfully!")
    else:
        print("Failed to modify event reporting rule.")


# Load JSON configuration from a file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None

router_ip = '192.168.1.1'  
username = 'admin' 
password = 'Admin123'  
config_file = 'config.json' 

# Authenticate with the router's API
access_token = authenticate(router_ip, username, password)

if access_token:

    rule_payload = load_config(config_file)


    create_event_reporting_rule(router_ip, access_token, rule_payload['create_data'])

if access_token:
    rule_id = 'cfg0292bd' 

    modify_payload = load_config(config_file)


    modify_event_reporting_rule(router_ip, access_token, rule_id, modify_payload['modify_data'])
