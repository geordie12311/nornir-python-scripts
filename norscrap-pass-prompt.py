#python script using getpass and inventory.defaults.password
#to avoid saving password anywhere, will prompt for password 
#before executing command on hosts in host file
import sys
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above getpass section is going to prompt the user for password
def credential_test(task):
    task.run(send_command, command="show ip int brief")

results = nr.run(credential_test)
print_result(results)