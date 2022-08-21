#simple python script using nornir_napalm plugin to get facts from hosts
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
#importing napalm_get from nornir_napalm

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
#above section is going to prompt the user to put in their password

def pull_info(task):
    task.run(task=napalm_get, getters=["get_facts"])
#function is using the getters syntax to get_facts from the hosts
results = nr.run(task=pull_info)
print_result(results)
