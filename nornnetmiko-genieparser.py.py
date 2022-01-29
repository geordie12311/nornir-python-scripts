#python script using genie parser and nornir_netmiko to output the show command
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
    interface_results = task.run(task=netmiko_send_command, command_string="show ip interface", use_genie=True)
    task.host["facts"] = interface_results.result
#function above is using use_genie=True argument to output the data from "show ip interface" 
# and present it as structured data. Note you need to use the .result atribute to parse the data
results = nr.run(task=test_this)
print_result(results)

