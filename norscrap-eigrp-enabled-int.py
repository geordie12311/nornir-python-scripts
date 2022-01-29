#Python script to check if EIGRP is enabled on a specific interface
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
    version_result = task.run(task=send_command, command="show ip interface")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    multicast_groups = task.host["facts"]["GigabitEthernet0/0"]["multicast_groups"]
    for multicast_ip in multicast_groups:
        if multicast_ip== "224.0.0.10":
            rprint(f"{task.host}'s int G0/0 has EIGRP enabled")
        else:
            rprint(f"{task.host}'s int G0/0 does not have EIGRP enabled")
#above function is going to create an object called pull_structured_data
#it is then going to csend the command (in this case show ip interface) to the hosts
#it is then going to put the output into structured data format and look for a multicast
#address of 224.0.0.10 (EIGRP) and then print to screen confirmation if EIGRP is enabled
#or not on each host
results = nr.run(task=pull_structured_data)


