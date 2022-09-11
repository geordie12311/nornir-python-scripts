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
# Python script using F filter to filter out specific hosts using the & which is the AND function using data in the host profile

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring Banner", file="animal_over15_banner.txt")
# creating the function to use send_configs_from_file to send the txt from the animal_over15_banner.txt file
animal_over_15 = nr.filter(F(rights__contains="ani") & F(age__ge=15))
# using F filter this time to filter hosts who's righs contain "ani" and who are over the age of 15
results = animal_over_15.run(task=banner_push)
print_result(results)