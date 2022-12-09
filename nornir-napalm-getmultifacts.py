#simple python script using nornir_napalm plugin to get facts and get interface info from hosts
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
#importing napalm_get from nornir_napalm

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def pull_info(task):
    task.run(task=napalm_get, getters=["get_facts", "get_interfaces"])
#function is using the getters syntax to get_facts and get_interfaces from the hosts
results = nr.run(task=pull_info)
print_result(results)
