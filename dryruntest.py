# Python script using napalm dry_run to validate configuration on hosts before being applied
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices

def dryrun_test(task):
    task.run(task=napalm_configure, filename="napalm-config.txt", dry_run=True)
# creating the function dryrun_test and using napalm_configure to send configuration from a text file
# note that dry_run=True which means Napalm will test and validate the configuration will be accepted by the hosts
# but will not actually apply it. You can change dry_run=False to apply the configuration once you have validated it

results = nr.run(task=dryrun_test)
print_result(results)

