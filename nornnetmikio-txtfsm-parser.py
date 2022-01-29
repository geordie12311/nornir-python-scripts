#python script usint textfsm and nornir_netmiko to output the show command
#in this case show clock in a structured data format. 
import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is initialising nornir and using getpass to prompt the user
#to enter their password
def test_this(task):
    clock_results = task.run(task=netmiko_send_command, command_string="show clock", use_textfsm=True)
    structured_result = clock_results.result
    print(structured_result)
#function above is using use_textfsm=True argument to output the data from "show clock" 
# and present it as structured data. Note you need to use the .result atribute to parse the data
results = nr.run(task=test_this)

