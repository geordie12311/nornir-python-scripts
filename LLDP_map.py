"""
Python LLDP-MAP Script
"""
import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command, netmiko_send_config

nr = InitNornir(config_file="config2.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def lldp_map(task):
    r = task.run(task=netmiko_send_command, command_string = "show lldp neighbors", use_genie=True)
    task.host["facts"] = r.result
    outer = task.host["facts"]
    interfaces = outer['interfaces']
    for intf in interfaces:
        local_intf = intf
        remote_keys = interfaces[intf]['port_id'].keys()
        for key in remote_keys:
            remote_port = key
            remote_id_keys = interfaces[intf]['port_id'][key]['neighbors'].keys()
            for key in remote_id_keys:
                remote_id = key

        lldp_config = task.run(netmiko_send_config,name="Automating LLDP Network Descriptions",config_commands=[
            "interface " + str(local_intf),
            "description Connected to " + str(remote_id) + " via its " + str(remote_port) + " interface"]
        )


results = nr.run(task=lldp_map)
print_result(results)