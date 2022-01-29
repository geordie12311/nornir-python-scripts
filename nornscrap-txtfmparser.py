#python script using textfsm and nornir_scrapli to output the show command
#in this case show clock in a structured data format. 
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is initialising nornir and using getpass to prompt the user
#to enter their password
def test_this(task):
    clock_results = task.run(task=send_command, command="show clock")
    structured_output = clock_results.scrapli_response.textfsm_parse_output()
    print(structured_output)
#function above is using textfsm_parse_output() object to output the data from "show clock"
#and present it as structured data
results = nr.run(task=test_this)

