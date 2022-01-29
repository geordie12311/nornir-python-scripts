#python script to use a username and password that has been saved in the ./bashrc file
import os 
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = os.environ["USERNAME"]
#above will look up the username saved in bash.rc
nr.inventory.defaults.password = os.environ["PASSWORD"]
#above will look up the password saved in bash.rc

def credential_test(task):
    task.run(send_command, command="show ip int brief")

results = nr.run(credential_test)
print_result(results)