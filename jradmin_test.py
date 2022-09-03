# Python script for junior admin users to run show commands. Note: need to ensure default file username is set to jradmin
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
password = getpass.getpass()
nr.inventory.defaults.password = password
#The above line is telling nornir where the config file is located

commands = input ("\nEnter Commands you want to send to the devices. Ensure they are comma seperated: ")
cmds = commands.split (",")

def push_show_commands(task):
    for cmd in cmds:
        task.run(task=send_command, command=cmd)

results = nr.run(task=push_show_commands)
print_result(results)

