#simple python script to check connectivity from all hosts to a single IP
import getpass
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result
#importing napalm_ping from nornir_napalm

nr = InitNornir(config_file="config.yaml")
password = getpass.getpass()
nr.inventory.defaults.password = password
def ping_test(task):
    task.run(task=napalm_ping, dest="99.99.99.99")
#function is using the dest syntax to ping 99.99.99.99 from all hosts
results = nr.run(task=ping_test)
print_result(results)
