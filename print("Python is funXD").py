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
# def create_event_reporting_rule(router_ip, access_token, rule_config):
#     rule_url = f"http://{router_ip}/api/services/events_reporting/config/"
#     headers = {'Authorization': f'Bearer {access_token}'}
#     payload = {
#   "id": "",
#   ".type": "rule"
# }
#     response = requests.post(rule_url, headers=headers, json=payload)

#     if response.status_code == 201:
#         print("Event reporting rule created successfully!")
#     else:
#         print("Failed to create event reporting rule.")
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
    with open(file_path, 'r') as file:
        config = json.load(file)
        return config

# Usage example
router_ip = '192.168.1.1'  # Replace with your router's IP address
username = 'admin'  # Replace with your router's username
password = 'Admin123'  # Replace with your router's password
config_file = 'config.json'  # Replace with the path to your JSON configuration file

# Authenticate with the router's API
access_token = authenticate(router_ip, username, password)

if access_token:
    rule_payload = {
        "id": "",
        ".type": "rule",
        # Add other necessary fields in the payload
    }
    create_event_reporting_rule(router_ip, access_token, rule_payload)


if access_token:
    rule_id = 'cfg0292bd' 
    modify_payload = {
  "data": {
    ".type": "rule",
    "action": "sendSMS",
    "enable": "1",
    "telnum": "+897456286",
    "event": "Config",
    "message": "Router name - %rn; Event type - %et; Event text - %ex; Time stamp - %ts",
    "recipient_format": "single",
    "eventMark": "wireless",
    "id": "cfg0292bd",
    "recipEmail": ""
  }
}
modify_event_reporting_rule(router_ip, access_token, rule_id, modify_payload)