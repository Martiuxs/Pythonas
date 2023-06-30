import requests
import json
import default_config
from authentication import authenticate

router_ip = default_config.router_ip
username = default_config.username
password = default_config.password
config_file = default_config.config_file

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
     raise ValueError(f"Error: Invalid JSON format in {file_path}")

def main():
    # Authenticate with the router's API
    access_token = authenticate(router_ip, username, password)

    if access_token:
        rule_payload = load_config(config_file)
        create_event_reporting_rule(router_ip, access_token, rule_payload['create_data'])

    if access_token:
        rule_id = 'cfg0192bd'
        modify_payload = load_config(config_file)
        modify_event_reporting_rule(router_ip, access_token, rule_id, modify_payload['modify_data'])

# Call the main function
if __name__ == '__main__':
    main()
