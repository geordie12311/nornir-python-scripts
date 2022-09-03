#python script using textfsm and nornir_netmiko to output the show command
#this script is using the command "show clock" to output structured data format. 
import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def test_this(task):
    clock_results = task.run(task=netmiko_send_command, command_string="show clock", use_textfsm=True)
    structured_result = clock_results.result
    print(structured_result)
#function above is using use_textfsm=True argument to output the data from "show clock" 
# and present it as structured data. Note you need to use the .result atribute to parse the data
results = nr.run(task=test_this)

