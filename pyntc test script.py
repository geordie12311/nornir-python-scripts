# Pyntc test script

import getpass
from nornir import InitNornir
from norinir_pyntc.task.pyntc_show import pyntc_show
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

results = nr.run(task=pyntc_show, command="show ip interface brief")
print_result(results)