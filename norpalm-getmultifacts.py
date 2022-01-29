from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
#importing napalm_get from nornir_napalm
nr = InitNornir(config_file="config.yaml")

def pull_info(task):
    task.run(task=napalm_get, getters=["get_facts", "get_interfaces"])
#function is using the getters syntax to get_facts and get_interfaces from the hosts
results = nr.run(task=pull_info)
print_result(results)