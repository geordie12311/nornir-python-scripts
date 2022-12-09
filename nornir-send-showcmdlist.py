#python script using nornir netmiko plugin to send multiple 
#show commands to hosts
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

command_list = ["show ntp config", "show ip interface brief", "show run"]
#using a command list to run multiple show commands
def show_cmd_test(task):
    for cmd in command_list: 
        task.run(task=netmiko_send_command, command_string=cmd)
#function is calling up the object cmd which is linked to command_list
results = nr.run(task=show_cmd_test)
print_result(results)
#setting the object results to ouptup of the task "show_cmd_task"
