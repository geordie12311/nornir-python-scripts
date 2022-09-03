#python script using nornir_scrapli plugin to send multiple configuration changes
#from a file called parser_config.txt
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result
#importing send_configs_from_file from nornir_scrapli to send configuration commands from a file

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def send_configs(task):
    task.run(task=send_configs_from_file, file="parser_config.txt")
#above function is going to use the send_configs to send configuration commands from a file

results = nr.run(task=send_configs)
#above line is setting an object results that is aligned to the task output
print_result(results)
