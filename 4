"""
INSTALL THE FOLLOWING:
pip3 install nornir
pip3 install nornir-scrapli
pip3 install nornir_utils
"""
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
# Python script using F filter to filter out specific hosts using data in the host profile

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring Banner", file="not_tennis_banner.txt")
# creating the function to use send_configs_from_file to send the txt from the not_tennis_banner.txt file
not_tennis = nr.filter(~F(location="court"))
# using F filter this time to filter out any host who has court in their data profile
results = not_tennis.run(task=banner_push)
print_result(results)