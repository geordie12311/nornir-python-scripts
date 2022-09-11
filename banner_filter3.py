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

# Python script using F filter to specific hosts using the pipe which is basically the OR function

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices

def banner_push(task):
    task.run(task=send_configs_from_file, name="Configuring the MOTD Banner", file="legend_or_tennis.txt")
# creating the function to use send_configs_from_file to send the txt from the tennis_legend_banner.txt file

legends_of_tennis = nr.filter(F(legend=True) | F(location="court"))
# applying a filter to check for legend or court to filter out hosts
results = legends_of_tennis.run(task=banner_push)
# running the results of the legends_on_the_court filter for the results
print_result(results)