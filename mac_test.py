import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint
#importing various python libraries needed for the script

nr = InitNornir(config_file="config4.yaml")#This is telling nornir which config file to use

user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

mac_list = []

target_mac = input("Enter the MAC address you want to find on the network: ")
#the above is creating the object target_mac to store the data input by the user

def pull_info(task):
    interface_result = task.run(task=send_command, command="show interfaces")
    task.host["facts"] = interface_result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]
    for interface in interfaces:
        try: 
            mac_addr = interfaces[interface]["mac_address"]
            if target_mac == mac_addr:
                mac_list.append(mac_addr)
                intf = interface
                print_info(task, intf)
        except KeyError:
            pass
"""
The above function is using send_command to show interfaces on all devices, then is parsing the data out 
using genie_parser and saving it "facts". It is then creating an object called mac_addr and parsing through 
the data to look for the mac addresses on each interface. It is then filtering through those mac addresses 
to find the target mac and also the local interface. It will also pass on key errors when it can't find a 
MAC address associated (such as loopback interfaces)
"""

def print_info(task, intf):
    rprint("\n[green] **** TARGET MAC ADDRESS FOUND ****[/green]")
    print(f"Target MAC address: {target_mac} is present on {task.host}'s {intf}\n")
    cdp_result = task.run(task=send_command, command="show cdp neighbors")
    task.host["cdpinfo"] = cdp_result.scrapli_response.genie_parse_output()
    dev_id = ""
    index = task.host["cdpinfo"]["cdp"]["index"]
    for num in index:
        local_intf = index[num]["local_interface"]
        if local_intf == intf:
            dev_id = index[num]["device_id"]
            port_id = index[num]["port_id"]

    ver_result = task.run(task=send_command, command="show version")
    task.host["verinfo"] = ver_result.scrapli_response.genie_parse_output()
    version = task.host["verinfo"]["version"]
    serial_num = version["chassis_sn"]
    oper_sys = version["os"]
    uptime = version["uptime"]
    version_short = version["version_short"]
    if dev_id:
        rprint("[magenta] *****REMOTE CONNECTION DETAILS*****[/magenta]")
        print(f"It is connected to {dev_id} on it's interface {port_id}\n")
    rprint("\n[cyan]******HOST DEVICE DETAILS******[/cyan]")
    print(f"Device hostname is: {task.host}")
    print(f"Device MGMT IP address is: {task.host.hostname}")    
    print(f"Device Serial Number: {serial_num}")
    print(f"Device version is: {version_short}")
    print(f"Device uptime is: {uptime}")
    print(f"Device OS version is: {oper_sys}\n")
    
nr.run(task=pull_info)
#using nr.run to run the function pull_info which will in turn run the print_info task
if target_mac not in mac_list:
    rprint("\n[red]Target MAC Address not found![/red]")