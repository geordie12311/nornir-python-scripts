 #python script using nornir_napalm getters to get facts
#and check vendor and uptime of network devices 
import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password

def pull_interfaces_info(task):
    interfaces_result = task.run(task=napalm_get, getters=["get_facts"])
    task.host["facts"] = interfaces_result.result
    uptime = task.host["facts"]["get_facts"]["uptime"]
    model = task.host["facts"]["get_facts"]["vendor"]
    #above will check the output of get facts for uptime and vendor
    if model == "Cisco":
        rprint(f"{task.host} is a [blue]Cisco[/blue] device. Uptime = {uptime}")
    #above will check if the vendor is Cisco and output the host and uptime if it matches
    if model == "Juniper":
        rprint(f"{task.host} is a [green]Juniper[/green] device. Uptime = {uptime}")
     #above will check if the vendor is Juniper and output the host and uptime if it matches   
    elif model == "EOS":
        rprint(f"{task.host} is a [yellow]Arista[/yellow] device. Uptime = {uptime}")  
     #above will check if the vendor is Arista and output the host and uptime if it matches 
results = nr.run(task=pull_interfaces_info)
