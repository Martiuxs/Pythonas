import json
import paramiko
import default_config
import requests
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
    
# SSH connection details
router_ip = default_config.router_ip
port = int(default_config.port)
username = 'root'
password = default_config.password



# SSH connection setup
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=router_ip, port=port, username=username, password=password)

# Add the new access point to the configuration file
# command = f"echo 'ssid={ssid}' >> /path/to/config/file"
# stdin, stdout, stderr = ssh.exec_command(command)

# Verify the changes in the web UI (you may need to adapt this step to your specific router)
# web_ui_command = "command_to_verify_changes_in_web_ui"
# stdin, stdout, stderr = ssh.exec_command(web_ui_command)

# Print the output of the web UI verification
# print(stdout.read().decode())

# Close the SSH connection
ssh.close()