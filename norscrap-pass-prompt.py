#python script using getpass and inventory.defaults.password to avoid saving password anywhere, 
#script will prompt for password before executing command on hosts in host file
import sys
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def credential_test(task):
    task.run(send_command, command="show ip int brief")

results = nr.run(credential_test)
print_result(results)
