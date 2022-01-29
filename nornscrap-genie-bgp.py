#Python script to check the uptime using genie parser of BGP neighbors on hosts in host file
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
    version_result = task.run(task=send_command, command="show ip bgp summary")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    neighbors = task.host["facts"]["vrf"]["default"]["neighbor"]
    for key in neighbors:
        uptime = neighbors[key]["address_family"][""]["up_down"]
        rprint(f"{task.host} neighbor {key} uptime value is {uptime}")
   #above function is going to create an object called pull_structured_data
#it is then going to csend the command (in this case show ip bgp summary) to the hosts
#it is then going to put the output into structured data format and look for up_down value
# of each neighbor and then then print the data to screen

results = nr.run(task=pull_structured_data)




