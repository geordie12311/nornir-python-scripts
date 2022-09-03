# Python script to prompt for username / passwords for groups that have different credentials
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located

selby_user = input("Enter your Selby_switch group username: ")
opus_user = input("Enter your Opus_switch group username: ")
selby_password = getpass.getpass(prompt="Enter the Selby_switch group password: ")
opus_password = getpass.getpass(prompt="Enter the Opus_switch group password: ")
nr.inventory.groups["Selby_switches"].username = selby_user
nr.inventory.groups["Opus_switches"].username = opus_user
nr.inventory.groups["Selby_switches"].password = selby_password
nr.inventory.groups["Opus_switches"].password = opus_password
#The above lines will prompt the user to enter their username and passwords for each group and use that input to connect to the devices in the groups.

def cred_test(task):
    task.run(task=send_command, command="show ip interface brief")

results = nr.run(task=cred_test)
print_result(results)
