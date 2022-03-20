#python script using genie parser and nornir_scrapli to output the show command
#in this case show ip interface in structured data format. 
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.functions import print_structured_result
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is initialising nornir and using getpass to prompt the user
#to enter their password
def test_this(task):
    interfaces_result = task.run(task=send_command, command="show ip interface")
#function above is creating an object to output the data from "show ip interface"
results = nr.run(task=test_this)
print_structured_result(results, parser="genie")
#and here we are using the genie parer to present the data as structured data

