"""
simple python script using nornir_scrapli to send a show command to a host
using a filter to prompt user to choose provide hostname and command
"""
import getpass
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command

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
Prompting user for hostname
"""
target = input("Enter the hostname: ")
target_host = nr.filter(name=target)

"""
Creating the function
to send the command
"""
def cconfig(test):
    test.run(task=send_command, command = ctarget)

'''
Prompting user for the 
show command they want to send
'''
ctarget = input("Insert show command you wish to run: ")
results = target_host.run(task = cconfig)

"""
Printing results 
to the screen
"""
print_result(results)
    
