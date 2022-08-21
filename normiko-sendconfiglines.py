#python script using nornir netmiko plugin to send configuration changes to hosts
import getpass
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
#importing netmiko send_config library

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is going to prompt the user to put in their password

def send_config_test(task):
    task.run(task=netmiko_send_config, config_commands=[
            "lldp run", 
            "username test1 priv 15 secret test123"
            ])
#function is sending the configuration commands to the hosts
results = nr.run(task=send_config_test)
print_result(results)
#setting the object results to output of the send_config_test function
