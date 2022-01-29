from distutils import command
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
command_list = ["show ip interface brief", "show version", "show run"]
#The above is creating an object that contains a list of commands
def show_command_test(task):
    for cmd in command_list:
        task.run(task=send_command, command=cmd)
#above function is then setting an objected called cmd which is then
#ran as the command when the send_command task is ran
results = nr.run(task=show_command_test)
#above line is setting an object results that is aligned to the task output
print_result(results)
#finally we print the data in the results object using print_results