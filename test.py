
import ipdb #importing ipdb to trace structured data
import getpass #importing getpass to handle the password for the hosts
from nornir import InitNornir #using nornir so importing InitNornir to initiate the script
from nornir_scrapli.tasks import send_command # importing scrapli send_command function
from nornir_salt.plugins.functions import FFun #importing FFun from salt for filtering hosts
from nornir_utils.plugins.functions import print_result #importing print_result to print the results to screen


nr = InitNornir(config_file="config.yaml") #Initiating Nornir using config.yaml as configuration file

userNamePrompt = "Enter your username: " #creating object for username prompt
passPrompt = "Enter your password: " #creating object for password prompt

targetPrompt = "Enter the hostnames of the devices you want to configure, (comma seperated): "#promting user to enter host(s) details
#cmdPrompt = "Enter the configuration commands to send to the hosts, (comma seperated):  "#promting user to enter command(s) to send to host(s)

userName = input(userNamePrompt) #using user inputted username to pass username to host(s)
password = getpass.getpass(passPrompt) #using getpass to pass the password to host(s)
nr.inventory.defaults.username = userName #using userName input for username to login
nr.inventory.defaults.password = password #using password input for password to authenticate

target = input(targetPrompt) #using user inputted hosts details for targets
#cmds = input(cmdPrompt) # using user inputted commands to send to hosts

filtered_hosts = FFun(nr, FL=target) # using FFun filter to filter the hosts
cmds = "show version"

output = filtered_hosts.run(send_command, command=cmds) #splitting the commands using the comma as the delimiter

results = nr.run(task=output) 
#print_result(results)
ipdb.set_trace()