#python script using nornir napalm plugin (napalm_ping) to ping an ip address from all hosts for connectivty checking
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result
#importing napalm_get from nornir_napalm

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is going to prompt the user to put in their password

def ping_test(task):
    task.run(task=napalm_ping, dest="99.99.99.99")
#function is using the getters syntax to get_facts from the hosts
results = nr.run(task=ping_test)
print_result(results)
