#python script using nornir napalm plugin (napalm_ping) to ping an ip address from all hosts for connectivty checking
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result
#importing napalm_get from nornir_napalm

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def ping_test(task):
    task.run(task=napalm_ping, dest="99.99.99.99")
#function is using the getters syntax to get_facts from the hosts
results = nr.run(task=ping_test)
print_result(results)
