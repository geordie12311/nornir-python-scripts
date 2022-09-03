#python script using napalm_ping plugin to ping destination over VRF
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result
#importing napalm_ping from nornir_napalm

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def ping_test(task):
    task.run(task=napalm_ping, dest="192.168.1.10", vrf="MGMT")
#function is using the dest and optional vrf syntax to ping an address over
#the MGMT vrf from all hosts 
results = nr.run(task=ping_test)
print_result(results)
