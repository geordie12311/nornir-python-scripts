#python script written to ask user to input show command they want to send to hosts
#it then uses Nornir_scrapli to send the show command entered and output to screen
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

commands = input ("\nEnter Commands you wish to send (comma seperated): ")
cmds = commands.split(",")

def push_show_commands(task):
    for cmd in cmds:
        task.run(task=send_command, command=cmd)

results = nr.run(task=push_show_commands)
print_result(results)

    
