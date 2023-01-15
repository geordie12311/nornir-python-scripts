#!/usr/bin/env python3
import getpass
from ipaddress import ip_network, ip_address
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result #importing print_result to print the results to screen
from rich import print as rprint

nr = InitNornir(config_file="config4.yaml") #Initiating Nornir using config.yaml as configuration file

### User credential section:
userNamePrompt = "Enter your username: " #creating object for username prompt
passPrompt = "Enter your password: " #creating object for password prompt

userName = input(userNamePrompt) #using user inputted username to pass username to host(s)
password = getpass.getpass(passPrompt) #using getpass to pass the password to host(s)
nr.inventory.defaults.username = userName #using userName input for username to login
nr.inventory.defaults.password = password #using password input for password to authenticate

target = input("Enter the target IP address: ")
ipaddr = ip_address(target)
my_list = []

def get_routes(task):
    response = task.run(task=send_command, command="show ip route")
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for prefix in prefixes:
        net = ip_network(prefix)
        if ipaddr in net:
            source_prot = prefixes[prefix]["source_protocol"]
            if source_prot == "connected":
                try:
                    outgoing_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]
                    for intf in outgoing_intf:
                        exit_intf = intf
                        my_list.append(f"{task.host} is connected to {target} via interface {exit_intf}")
                except KeyError:
                    pass
            else:
                try:
                    next_hop_list = prefixes[prefix]["next_hop_list"]
                    for key in next_hop_list:
                        next_hop = next_hop_list[key]["next_hop"]
                        my_list.append(f"{task.host} can reach {target} via next hop {next_hop} ({source_prot})")
                except KeyError:
                    pass

nr.run(task=get_routes)
sorted_list = sorted(my_list)
rprint(sorted_list)
                        