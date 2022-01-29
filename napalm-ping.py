from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result
#importing napalm_get from nornir_napalm
nr = InitNornir(config_file="config.yaml")

def ping_test(task):
    task.run(task=napalm_ping, dest="99.99.99.99")
#function is using the getters syntax to get_facts from the hosts
results = nr.run(task=ping_test)
print_result(results)