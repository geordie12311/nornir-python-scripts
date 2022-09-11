"""
Install the following libraries:
pip3 install nornir
pip3 install nornir_scrapli
pip3 install nornir_utils
"""
# Python script to filter on specific host attributes and apply site specifci banners
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs_from_file
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
# importing F filter from nornir to use for filtering

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring the MOTD Banner", file="legend_banner.txt")

legends = nr.filter(F(legend=True))
results = legends.run(task=banner_push)
print_result(results)