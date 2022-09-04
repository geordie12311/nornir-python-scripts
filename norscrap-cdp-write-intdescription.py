"""
python script using nornir_scrapli to use cdp neighbor info to automatically write 
descriptions on the host interfaces to show what device it connects 
to and which remote interface
"""
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def pull_structured_data(task):
    cdp_result = task.run(task=send_command, command="show cdp neighbor")
    task.host["facts"] = cdp_result.scrapli_response.genie_parse_output()
    cdp_index = task.host["facts"]["cdp"]["index"]
    for num in cdp_index:
        local_intf = cdp_index[num]["local_interface"]
        remote_intf = cdp_index[num]["port_id"]
        remote_device = cdp_index[num]["device_id"]
        config_commands = [f"interface {local_intf}", f"description Connected to {remote_device} via its interface {remote_intf}"]
        task.run(task=send_configs, configs=config_commands)
# Above function is going to create an object called pull_structured_data it is then going to send the command "show CDP neighor" to the hosts and then cycle
# through the data to find the local, remote interfaces. It is then going to use scrapli send_configs to write the description to each interface on the host 
# i.e. Connected to x device via its interface

results = nr.run(task=pull_structured_data)
print_result(results)
#script is then going to output the results to the screen to verify success
