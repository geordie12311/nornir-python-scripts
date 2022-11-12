import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command
from nornir_utils.plugins.functions import print_result
#importing netmiko send_config library

nr = InitNornir(config_file="config3.yml")
#The above line is telling nornir where the config file is located
user = input("Please enter your username: ")
password = getpass.getpass(prompt="Please enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

swport_list = []

switchport = input("Please enter Switch port numbers you wish to configure (example: 0/1 0/2 etc) seperated by a space: ")
vlanid = input("Please enter the Data VLAN number you wish to enable on the ports (example 10): ")
voicevlan = input("Please enter the Voice VLAN you wish to enable on the ports or leave blank if Voice is not required): ")

swport_list.append(switchport)
for port in swport_list:
    print(port)
