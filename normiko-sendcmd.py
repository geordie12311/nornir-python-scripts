#python script using nornir_netmiko to send show commands and print results
import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
#importing netmiko send_command library

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is going to prompt the user to put in their password

def show_cmd_test(task):
    task.run(task=netmiko_send_command, command_string="cdp enable")
#the function is using netmiko_send_command to send a command string to the devices
results = nr.run(task=show_cmd_test)
print_result(results)
#setting the object results to ouptup of the task "show_cmd_task"
