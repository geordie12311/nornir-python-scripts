#python script written to ask user to input show command they want to send to hosts
#it then uses Nornir_scrapli to send the show command entered and output to screen
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

commands = input ("\nEnter Commands you wish to send (comma seperated): ")
cmds = commands.split(",")

def push_show_commands(task):
    for cmd in cmds:
        task.run(task=send_command, command=cmd)

results = nr.run(task=push_show_commands)
print_result(results)

    
