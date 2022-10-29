#python script using nornir netmiko plugin to send configuration changes to hosts
import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
#importing netmiko send_config library

nr = InitNornir(config_file="config2.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def send_config_test(task):
    task.run(task=netmiko_send_config, config_commands=[
            "lldp run", 
            "cdp run",
            "do wr"
            ])
#function is sending the configuration commands to the hosts
results = nr.run(task=send_config_test)
print_result(results)
#setting the object results to output of the send_config_test function
