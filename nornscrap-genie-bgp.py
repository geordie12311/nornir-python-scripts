#Python script to check the uptime using genie parser of BGP neighbors on hosts
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint 

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

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




