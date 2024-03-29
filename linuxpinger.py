"""
Python Pinger script
"""
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

target_list = []
failed_list = []

def get_ip(task):
    result = task.run(task=send_command, command="show ip interface brief")
    task.host["facts"] = result.scrapli_response.genie_parse_output()
    interfaces = task.host["facts"]["interface"]
    for intf in interfaces:
        if intf.startswith("Loop"):
            ip_addr = interfaces[intf]["ip_address"]
            target_list.append(ip_addr)

def ping_test(task):
    for ip_address in sorted_list:
        result = task.run(task=send_command, command="ping " + ip_address)
        response = result.result
        if not "!!!" in response:
            failed_list.append(f"{task.host} cannot ping {ip_address}")


nr.run(task=get_ip)
sorted_list = sorted(target_list)
nr.run(task=ping_test)
if failed_list:
    sorted_fails = sorted(failed_list)
    rprint(sorted_fails)
else:
    rprint("[green]All pings were successful[/green]")