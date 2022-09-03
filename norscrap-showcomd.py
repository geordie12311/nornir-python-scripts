#simple python script to run a show command on hosts
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

def show_command_test(task):
    task.run(task=send_command, command="show ip interface brief")

results = nr.run(task=show_command_test)
print_result(results)
