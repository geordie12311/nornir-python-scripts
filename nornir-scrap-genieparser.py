#python script using genie parser and nornir_scrapli to output the show command
#in this case show ip interface in structured data format. 
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.functions import print_structured_result
from nornir_utils.plugins.functions import print_result
import ipdb

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def test_this(task):
    interfaces_result = task.run(task=send_command, command="show ip interface")
#function above is creating an object to output the data from "show ip interface"
results = nr.run(task=test_this)
print_structured_result(results, parser="genie")
#and here we are using the genie parer to present the data as structured data

