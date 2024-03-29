#python script used to rollback to a previously saved image held on flash
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
#importing send_command from nornir_scrapli as the command that we need to send is at the
#enable prompt not configuration therefore send_config would be incorrect

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

def rollin_back_to_goldimage(task):
    task.run(task=send_command, command="configure replace flash:goldimage1 force")
#the function above is going to send the command to the hosts to rollback to the
#gold image configuration file saved in flash
results = nr.run(task=rollin_back_to_goldimage)
print_result(results)

