#python script to send configuration changes from a text file
from nornir import InitNornir
from nornir_scrapli.tasks import send_commands_from_file
from nornir_utils.plugins.functions import print_result
#importing send_commands_from_file from nornir_scrapli to send a list of commands from a file
nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located

def show_command_test(task):
    task.run(task=send_commands_from_file, file="random_commands.txt")
#above function is going to use the send_commands_from_file task to send
# the commands listed in the random_commands.txt file

results = nr.run(task=show_command_test)
#above line is setting an object results that is aligned to the task output
print_result(results)
