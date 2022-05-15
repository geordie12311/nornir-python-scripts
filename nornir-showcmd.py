#simple python script using nornir_scrapli to send a show command to hosts
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir import InitNornir

nr = InitNornir(config_file="config1.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password

results = nr.run(task=send_command, command="show version")
print_result(results)
