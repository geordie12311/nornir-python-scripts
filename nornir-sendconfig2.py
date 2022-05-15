#python script using norni_scrapli plugin to send single configuration
#change to hosts
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_config
from nornir_utils.plugins.functions import print_result
#importing send_config from nornir_scrapli to send a configuration change
nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located

password = getpass.getpass()
nr.inventory.defaults.password = password

def send_config_test(task):
    task.run(task=send_config, config="ntp server 10.10.10.150")
#above function is going to use the send_config to send a configuration command

results = nr.run(task=send_config_test)
#above line is setting an object results that is aligned to the task output
print_result(results)
