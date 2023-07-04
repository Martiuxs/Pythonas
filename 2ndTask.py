import json
import paramiko
import default_config
import requests
from authentication import authenticate

# Load the configuration from JSON file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except json.JSONDecodeError:
     raise ValueError(f"Error: Invalid JSON format in {file_path}")

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
   
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(default_config.router_ip, int(default_config.port), default_config.ssh_username, default_config.password)
    print("SSH connection successful!")

     # Read existing content of the wireless file
    command = "cat /etc/config/wireless"
    stdin, stdout, stderr = ssh.exec_command(command)
    existing_content = stdout.read().decode()

    # Modify the existing content by adding the new configuration lines
    modified_content = existing_content.strip() + '\n' + '\n'.join(load_config(default_config.config_wifi))
    print(default_config.config_wifi)

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
    assign(authenticate(default_config.router_ip, default_config.username, default_config.password))
    ssh.close()