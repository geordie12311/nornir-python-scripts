#python script using nornir_scrapli to send config change
#to hosts will prompt for password
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

password = getpass.getpass()
nr.inventory.defaults.password = password
#above getpass section is going to prompt the user for password

def random_config(task):
     task.run(task=send_config, config=f"ntp server {task.host['ntp_server']}")
#the above function is sending ntp_server details for each host defined 
#in the data option in the host file
results = nr.run(task=random_config)
print_result(results)
