"""
This script will take a target IP address and determine
how each device will process that IP address
"""
import getpass
import os
from ipaddress import ip_network, ip_address
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

CLEAR = "clear"
os.system(CLEAR)

target = input("Enter the target IP: ")
ipaddr = ip_address(target)
my_list = []

def get_routes(task):
    """
    Parse routing table and determine if target IP finds a match
    """
    response = task.run(task=send_command, command="show ip route")
    task.host["facts"] = response.scrapli_response.genie_parse_output()
    prefixes = task.host["facts"]["vrf"]["default"]["address_family"]["ipv4"]["routes"]
    for prefix in prefixes:
        net = ip_network(prefix)
        if ipaddr in net:
            source_proto = prefixes[prefix]["source_protocol"]
            if source_proto == "connected":
                try:
                    outgoing_intf = prefixes[prefix]["next_hop"]["outgoing_interface"]
                    for intf in outgoing_intf:
                        exit_intf = intf
                        my_list.append(
                            f"{task.host} is connected to {target} via interface {exit_intf}"
                        )
                except KeyError:
                    pass
            else:
                try:
                    next_hop_list = prefixes[prefix]["next_hop"]["next_hop_list"]
                    for key in next_hop_list:
                        next_hop = next_hop_list[key]["next_hop"]
                        exit_intf = next_hop_list[key]["outgoing_interface"]
                        my_list.append(
                            (
                                f"{task.host} can reach {target} via interface {exit_intf}"
                                f" ~~ next hop: {next_hop} ({source_proto})"
                            )
                        )
                except KeyError:
                    pass

results = nr.run(task=get_routes)
if my_list:
    sorted_list = sorted(my_list)
    rprint(sorted_list)
else:
    rprint(f"{target} is not reachable")
