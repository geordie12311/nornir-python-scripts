#python script to save the running configuration to flash as a gold image
from nornir import InitNornir
from nornir_scrapli.tasks import send_interactive
from nornir_utils.plugins.functions import print_result
#importing send_interactive from nornir_scrapli to send interactive commands

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def commit_goldimage_flash(task):
    cmds = [("copy run flash:goldimage1", "Destination filename"), ("\n", f"{task.host}#")]
    task.run(task=send_interactive, interact_events=cmds)
#function above is going to copy running configuration to a file called goldimage1 in flash
#the function is going to use the task.host to run through each host in the hostfile
#note: you need to add a # after {task.host} due to the prompt i.e. R1#

results = nr.run(task=commit_goldimage_flash)
print_result(results)
#printing out the results from the function to the screen
