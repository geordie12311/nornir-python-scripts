""" Python script using nornir_scrapli, nornir_salt (FFun) as a filter
to send a set of configuration commands to a set of hosts. Script will prompt 
the user to provide credentials and the hostnames they want to configure
and also the list of configuration commands """

import getpass #importing getpass to handle the password for the hosts
from nornir import InitNornir #using nornir so importing InitNornir to initiate the script
from nornir_scrapli.tasks import send_configs # importing scrapli to send configuration commands
from nornir_salt.plugins.functions import FFun #importing FFun for filtering
from nornir_utils.plugins.functions import print_result #importing print_result to print the results to screen

nr = InitNornir(config_file="config.yaml") #Initiating Nornir using config.yaml as configuration file

userNamePrompt = "Enter your username: " #creating object for username prompt
passPrompt = "Enter your password: " #creating object for password prompt

targetPrompt = "Enter the hostnames of the devices you want to configure, (comma separated list): "#promting user to enter host(s) details
cmdPrompt = "Configuration commands to send, (comma separated list):  "#promting user to enter command(s) to send to host(s)

userName = input(userNamePrompt) #using user inputted username to pass username to host(s)
password = getpass.getpass(passPrompt) #using getpass to pass the password to host(s)
nr.inventory.defaults.username = userName #using userName input for username to login
nr.inventory.defaults.password = password #using password input for password to authenticate

target = input(targetPrompt) #using user inputted hosts details for targets
cmds = input(cmdPrompt) # using user inputted commands to send to hosts

filtered_hosts = FFun(nr, FL=target) # using FFun filter to filter the hosts
output = filtered_hosts.run(send_configs, configs=cmds.split(",")) #splitting the commands using the comma as the delimiter

results = (output) #creating results object to capture output from the task
print_result(results) #printing out the results from the task