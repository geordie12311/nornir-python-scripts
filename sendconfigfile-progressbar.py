#python script using netmiko plugin send_config to send configuration from a text file "randomconfig.txt"
# script also includes a progress bar that will display on the screen
import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from tqdm import tqdm
#importing netmiko send_config library

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def send_config_test(task, progress_bar):
    task.run(task=netmiko_send_config, config_file="netmiko-randomconfig.txt")
    progress_bar.update()
#function is sending the configuration commands in the file to the hosts and linking to the projgress bar

with tqdm(total=len(nr.inventory.hosts)) as progress_bar:
    results = nr.run(task=send_config_test, progress_bar=progress_bar)
# above is going to use tqdm to create a progress bar to show script progress as it pushes the config out to each host

print_result(results)
#setting the object results to output of the send_config_test function
