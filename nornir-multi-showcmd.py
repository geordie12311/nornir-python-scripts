#python script using nornir_scrapli to send multiple show commands
#user will be prompted to add show commands on screen
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
#importing send_commands from nornir_scrapli to send multiple commands

nr = InitNornir(config_file="config4.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

commands = input ("\nEnter Commands you wish to send (comma seperated): ")
cmds = commands.split(",")
#above is going to display Enter commands on the screen and pass commands entered
#to the function below
def push_show_commands(task):
    for cmd in cmds:
        task.run(task=send_command, command=cmd)
#above function is going to take the commands input by the user and 
# use send_commands task to send those commands to the host

results = nr.run(task=push_show_commands)
#above line is setting an object results that is aligned to the task output
print_result(results)
#finally we print the data in the results object using print_results
