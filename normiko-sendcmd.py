#python script using nornir_netmiko to send show commands and print results
import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
#importing netmiko send_command library

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def show_cmd_test(task):
    task.run(task=netmiko_send_command, command_string="show ip int brief")
#the function is using netmiko_send_command to send a command string to the devices
results = nr.run(task=show_cmd_test)
print_result(results)
#setting the object results to ouptup of the task "show_cmd_task"
