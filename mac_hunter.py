import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as pprint
#importing various python libraries needed for the script

nr = InitNornir(config_file="config4.yaml")#This is telling nornir which config file to use

user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

target_mac = input("Enter the MAC address you want to find on the network: ")
#the above is creating the object target_mac to store the data input by the user

def pull_info(task):
    interface_result = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = interface_result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for interface in interfaces:
        mac_addr = interfaces[interface]["mac_address"]
        if target_mac == mac_addr:
            intf = interface
            print_info(task, intf)
#The above function is using send_command to show interfaces on all devices, then is parsing the 
#data out using genie_parser and saving it "facts". It is then creating an object called mac_addr
#and parsing through the data to look for the mac addresses on each interface. It is then filtering
#through those mac addresses to find the target mac and also the local interface

def print_info(task, intf):
    print(f"\nTarget MAC address: {target_mac} is present on {task.host}'s {intf}")
    cdp_result = task.run(task=send_command, command="show cdp neighbors")
    task.host["cdpinfo"] = cdp_result.scrapli_response.genie_parse_output()
    index = task.host["cdpinfo"]["cdp"]["index"]
    for num in index:
        local_intf = index[num]["local_interface"]
        if local_intf == intf:
            dev_id = index[num]["device_id"]
            port_id = index[num]["port_id"]
            print(f"It is connected to {dev_id} on it's interface {port_id}\n")
#The above function is using the command "show cdp neighbors", to identify the remote port
#that the local port with the target MAC address is connected to and will then print out
#both the device / interface where the target MAC address resides and also details of the 
#device and remote interface it is connected to

nr.run(task=pull_info)
#using nr.run to run the function pull_info which will in turn run the print_info task