import requests
import paramiko
import json
import default_config
import time
from authentication import authenticate


router_ip = default_config.router_ip
username = default_config.username
password = default_config.password
config_file = default_config.config_file

# def create_event_reporting_rule(router_ip, access_token, rule_payload):
#     rule_url = f"http://{router_ip}/api/services/events_reporting/config/"
#     headers = {'Authorization': f'Bearer {access_token}'}

#     response = requests.post(rule_url, headers=headers, json=rule_payload)

#     if response.status_code == 201:
#         print("Event reporting rule created successfully!")
#     else:
#         print("Failed to create event reporting rule.")
        
# def modify_event_reporting_rule(router_ip, access_token, rule_id, modify_payload):
#     rule_url = f"http://{router_ip}/api/services/events_reporting/config/{rule_id}"
#     headers = {'Authorization': f'Bearer {access_token}'}

#     response = requests.put(rule_url, headers=headers, json=modify_payload)

#     if response.status_code == 200:
#         print("Event reporting rule modified successfully!")
#     else:
#         print("Failed to modify event reporting rule.")

def create_event_reporting_rule(token):
  
    url = "http://192.168.1.1/api/services/events_reporting/config"

    payload = json.dumps({
    "data": {
        ".type": "rule",
        "event": "Config",
        "eventMark": "wireless",
        "action": "sendSMS",
        "enable": "1",
        "message": "Router name - %rn; Event type - %et; Event text - %ex; Time stamp - %ts",
        "recipEmail": "",
        "emailgroup": "",
        "subject": "",
        "recipient_format": "single",
        "telnum": "+37063032518"
    }
    })
    headers = {
    'Authorization': f"Bearer {token}",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 201:
        print("Event reporting rule created successfully!")
    else:
        print("Failed to create event reporting rule.")
    # print(response.text)


def create_wifi_config(token):
 
    url = "http://192.168.1.1/api/network/wireless/devices/config/radio0/interfaces"

    payload = json.dumps({
    "data": {
        "enabled": "1",
        ".type": "wifi-iface",
        "ssid": "Test1234",
        "disassoc_low_ack": "1",
        "wmm": "1",
        "mode": "ap",
        "short_preamble": "1",
        "network": "lan",
        "hidden": "0",
        "key": "",
        "isolate": "0",
        "dtim_period": "",
        "wpa_group_rekey": "",
        "skip_inactivity_poll": "0",
        "max_inactivity": "",
        "max_listen_interval": ""}
    })
    headers = {
    'Authorization': f"Bearer {token}",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 201:
        print("Wifi Configured Successfully")
    else:
        print("Failed to configure wifi")
    # print(response.text)

# Load JSON configuration from a file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except json.JSONDecodeError:
     raise ValueError(f"Error: Invalid JSON format in {file_path}")

# def assign(token):
#     url = "http://192.168.1.1/api/bulk"

#     payload = json.dumps({
#     "data": [
#         {
#         "method": "PUT",
#         "endpoint": "/api/network/wireless/devices/config/radio0/interfaces",
#         "data": [
#             {
#             "enabled": "1",
#             ".type": "wifi-iface",
#             "id": "default_radio0"
#             },
#         ],
#         "awaitNetwork": True
#         }
#     ]
#     })
#     headers = {
#     'Authorization': f"Bearer {token}",
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
#     print('Network Restarted')
    
def main():
    # Authenticate with the router's API
    access_token = authenticate(router_ip, username, password)

    if access_token:
        rule_payload = load_config(config_file)
        # create_event_reporting_rule(router_ip, access_token, rule_payload['create_data'])
        # time.sleep(5)
        # rule_id = 'cfg0192bd'
        # modify_payload = load_config(config_file)
        # modify_event_reporting_rule(router_ip, access_token, rule_id, modify_payload['modify_data'])
        # time.sleep(5)
        create_event_reporting_rule(access_token)
        time.sleep(5)
        create_wifi_config(access_token)
    else:
        print("Failed to authenticate with the router's API.") 

        
    # create_wifi_config = load_config(default_config.config_wifi)    
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # try:
    #     ssh.connect(default_config.router_ip, int(default_config.port), default_config.ssh_username, default_config.password)
    #     print("SSH connection successful!")
    #     command = "cat /etc/config/wireless"
    #     stdin, stdout, stderr = ssh.exec_command(command)
    #     existing_content = stdout.read().decode()

    #     modified_content = existing_content.strip() + '\n' + '\n'.join(load_config(default_config.config_wifi))
    #     print('Config Added Successfully')
    
    #     command = f"echo '{modified_content}' > /etc/config/wireless"
    #     stdin, stdout, stderr = ssh.exec_command(command)
    #     print("Configuration lines added to /etc/config/wireless file.")
    #     assign(authenticate(default_config.router_ip, default_config.username, default_config.password))
    # except paramiko.AuthenticationException:
    #     print("Authentication failed. Please check your credentials.")
    # except paramiko.SSHException as ssh_exception:
    #     print(f"SSH connection error: {str(ssh_exception)}")
    # except Exception as e:
    #     print(f"Error: {str(e)}")
    # finally:
    #     ssh.close()
    #     print("SSH connection closed.")     

if __name__ == '__main__':
    main()