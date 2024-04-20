"""
Simple scrapli script to connect to multiple hosts
This example uses connection manager to manage,
opening and closing the connection
"""

from scrapli.driver.core import IOSXEDriver #importing IOSXEDriver from scrapli

devices = [
    {
        "host": "lab-sw1",
        "auth_username": "cisco",
        "auth_password": "cisco123",
        "auth_strict_key": False,
        "ssh_config_file": True
    }    
]
# above, creating an object called devices to hold the hostname and credentials that scrapli will use to connect

for device in devices:
    with IOSXEDriver(**device) as conn: #using a for loop with content manager to connect to the hosts
        response = conn.send_command("Show IP interface brief") #creating the object response and using send_command to send command to hosts
    
print(response.result) #printing the response results to screen