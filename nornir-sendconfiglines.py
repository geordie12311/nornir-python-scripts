#python script using nornir_scrapli to send config lines to hosts
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def send_configs_test(task):
    task.run(task=send_configs, configs=["lldp"])
#above function is going to use the send_configs to send a list of configuration commands

results = nr.run(task=send_configs_test)
#above line is setting an object results that is aligned to the task output
print_result(results)
