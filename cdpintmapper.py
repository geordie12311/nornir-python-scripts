"""
python script using nornir to use cdp neighbor info to automatically write 
descriptions on the host interfaces based on the output 
"""

import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_title, print_result
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command
# Importing the python libraries needed for the script

nr = InitNornir(config_file="config6.yaml")
# creating an object called "nr" and telling nornir which config file to use for the script

user = input("Please enter your username: ")
password = getpass.getpass(prompt="Please enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
# Using getpass to prompt the user to enter their username and password and use that input to connect to the devices
# Note by default getpass does not display the entered password

def cdp_map(task):
    r = task.run(task=netmiko_send_command, command_string = "show cdp neighbor", use_genie=True)
    task.host["facts"] = r.result
    outer = task.host["facts"]
    indexer = outer['cdp']['index']
    for idx in indexer:
        local_intf = indexer[idx]['local_interface']
        remote_port = indexer[idx]['port_id']
        remote_id = indexer[idx]['device_id']
        cdp_config = task.run(netmiko_send_config,name="Automating CDP Network Descriptions",config_commands=[
            "interface " + str(local_intf),
            "description Connected to " + str(remote_id) + " via its " + str(remote_port) + " interface"]
        )
# Above function is saving the output from show cdp neigh ar "r" and then saving is a facts. It is then using indexer to identify
# the local interface, remote port and remote device id then using that to writ the description to the interface

results = nr.run(task=cdp_map)
print_result(results)
# Printing the output from the task cdp_map and displaying it on the screen