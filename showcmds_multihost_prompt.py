"""
Python script using nornir_scrapli, nornir_salt (FFun) as a filter
to send a set of show commands to a list of hosts. Script will prompt 
the user to provide credentials and provide hostnames + list of show commands
"""
import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_commands
from nornir_salt.plugins.functions import FFun

"""
Initiating Nornir
"""
nr = InitNornir(config_file="config.yaml")

"""
Prompting user for username
and password. Using getpass for password
"""
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password

"""
Prompting user for the hostnames 
and list of show commands
"""
target = input("Choose hosts, comma separated list: ")
cmds = input("Commands to send, comma separated list:  ")

"""
filering the hosts and sending the commands
split by line using the , as the delimiter"""
filtered_hosts = FFun(nr, FL=target)
output = filtered_hosts.run(send_commands, commands=cmds.split(","))

"""
printing out the results 
"""
results = (output)
print_result(results)