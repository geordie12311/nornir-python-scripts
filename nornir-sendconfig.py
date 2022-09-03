#python script using nornir_scrapli to send config change
#to hosts will prompt for password
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def random_config(task):
     task.run(task=send_config, config=f"ntp server {task.host['ntp_server']}")
#the above function is sending ntp_server details for each host defined 
#in the data option in the host file
results = nr.run(task=random_config)
print_result(results)
