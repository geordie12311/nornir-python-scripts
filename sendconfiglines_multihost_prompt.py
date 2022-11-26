"""
Python script using nornir_scrapli, nornir_salt (FFun) as a filter
to send a set of configuration commands to a set of hosts. Script will prompt 
the user to provide credentials and the hostnames they want to configure
and also the list of configuration commands
"""
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_salt.plugins.functions import FFun
from nornir_utils.plugins.functions import print_result

"""
Initiating Nornir
"""
nr = InitNornir(config_file="config.yaml")

"""
Prompting user for username
and password. Using getpass for password
"""
userNamePrompt = "Enter your username: "
passPrompt = "Enter your password: "

userName = input(userNamePrompt)
password = getpass.getpass(passPrompt)
nr.inventory.defaults.username = userName
nr.inventory.defaults.password = password

"""
Prompting user for the hostnames 
and list of configuration commands
"""
target = input("list the hosts you want to configure, (comma separated list): ")
cmds = input("Configuration commands to send, (comma separated list):  ")

"""
filering the hosts and sending the commands
split by line using the , as the delimiter
"""
filtered_hosts = FFun(nr, FL=target)
output = filtered_hosts.run(send_configs, configs=cmds.split(","))

"""
printing out the results 
"""
results = (output)
print_result(results)