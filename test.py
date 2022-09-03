import getpass
import time
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

rprint("[bold red on yellow]*****THIS SCRIPT WILL RUN 'SHOW RUN' COMMAND AND DISPLAY THE OUTPUT FROM ALL HOSTS*****[/bold red on yellow]")
#displaying a banner to confirm what the script does to the use

results = nr = nr.run(task=send_command, command="show run")
print_result(results)
