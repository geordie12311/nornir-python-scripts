#python script to print out cdp neighbor information for all hosts in host file
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint 

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is going to prompt the user to put in their password

def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show cdp neighbor")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    cdp_index = task.host["facts"]["cdp"]["index"]
    for num in cdp_index:
        local_intf = cdp_index[num]["local_interface"]
        remote_intf = cdp_index[num]["port_id"]
        remote_device = cdp_index[num]["device_id"]
        rprint(f"{task.host} {local_intf} is connected to {remote_device} {remote_intf}")
#above function is going to create an object called pull_structured_data
#it is then going to send the command "show CDP neighor" to the hosts and then cycle
# through the data to find the local, remote interfaces and then print out the data
# with the hostname to show which devices are connected to which interface

results = nr.run(task=pull_structured_data)

#ipdb.set_trace()
