import json
import paramiko
import default_config
import requests
import socket
# Load the configuration from JSON file
with open('config.json') as f:
    config = json.load(f)

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
    
def assign(token):
    url = "http://192.168.1.1/api/bulk"

    payload = json.dumps({
    "data": [
        {
        "method": "PUT",
        "endpoint": "/api/network/wireless/devices/config/radio0/interfaces",
        "data": [
            {
            "enabled": "1",
            ".type": "wifi-iface",
            "id": "default_radio0"
            },
        ],
        "awaitNetwork": True
        }
    ]
    })
    headers = {
    'Authorization': f"Bearer {token}",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
   
# SSH connection details
router_ip = default_config.router_ip
port = int(default_config.port)
username = 'root'
password = default_config.password

config_lines = [
     "",
 "config wifi-iface",
    "\toption encryption 'none'",
    "\toption device 'radio0'",
    "\toption mode 'ap'",
    "\toption wifi_id 'wifi1'",
    "\toption skip_inactivity_poll '0'",
    "\toption network 'lan'",
    "\toption hidden '0'",
    "\toption ieee80211r '0'",
    "\toption isolate '0'",
    "\toption ssid 'Testas123456'",
    "\toption short_preamble '1'",
    "\toption disassoc_low_ack '1'",
    "\toption short_preamble 1",
    "\toption ieee80211r 0",
    "\toption encryption none",
    "\toption wifi_id wifi2"
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(hostname=router_ip, port=port, username=username, password=password)
    print("SSH connection successful!")

     # Read existing content of the wireless file
    command = "cat /etc/config/wireless"
    stdin, stdout, stderr = ssh.exec_command(command)
    existing_content = stdout.read().decode()

    # Modify the existing content by adding the new configuration lines
    modified_content = existing_content.strip() + '\n' + '\n'.join(config_lines)

    # Write the modified content back to the wireless file
    command = f"echo -e '{modified_content}' > /etc/config/wireless"
    stdin, stdout, stderr = ssh.exec_command(command)
    print("Configuration lines added to /etc/config/wireless file.")
    
except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
except paramiko.SSHException as ssh_exception:
    print(f"SSH connection error: {str(ssh_exception)}")
except Exception as e:
    print(f"Error: {str(e)}")
finally:
  
    ssh.close()