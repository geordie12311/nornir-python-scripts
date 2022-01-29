#python script to check for specific IOS version on hosts in host file
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint 

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password

def pull_structured_data(task):
    version_result = task.run(task=send_command, command="show version")
    task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    version = task.host["facts"]["version"]["version_short"]
    if version =="15.7":
        rprint(f"{task.host}:[green]Version check passed")
    else:
       rprint(f"{task.host}: [red]Version check failed")
#above function is going to create an object called pull_structured_data
#it is then going to create a 2nd object called facts and parse it through genie
#to provide structured data output. Then the object version is going to go down through
#the structure and find "version_short" and then the if statement is going to check for
#version 15.7, if it finds it then it will print "version check" passed along with hostname
#if it finds a different version it will be picked up by the else statement and print out
#"version check failed"

results = nr.run(task=pull_structured_data)


