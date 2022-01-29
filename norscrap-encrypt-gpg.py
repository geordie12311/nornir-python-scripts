#the script is writen to use a username and password that has  
#been saved in an encrypted file encrypted using gpg.
#note: you have to decrypt the file when running the script  
import os
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

nr.inventory.defaults.username = os.environ["DEFAULT_USERNAME"]
nr.inventory.defaults.password = os.environ["DEFAULT_PASSWORD"]
#above will lookup default_username and password which will be loaded into memory when 
#the you decrypt the encrypted file 

def credential_test(task):
    task.run(send_command, command="show ip int brief")

results = nr.run(credential_test)
print_result(results)