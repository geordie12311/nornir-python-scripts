# Test python runbook to pull ntp_server details from host file and apply to configuration
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is going to prompt the user to put in their password

def random_config(task):
    task.run(task=send_config, config=f"ntp server {task.host['ntp_server']}")

results = nr.run(task=random_config)
print_result(results)