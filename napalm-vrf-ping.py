#python script using napalm_ping plugin to ping destination over VRF
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result
#importing napalm_ping from nornir_napalm
nr = InitNornir(config_file="config.yaml")

def ping_test(task):
    task.run(task=napalm_ping, dest="192.168.1.10", vrf="MGMT")
#function is using the dest and optional vrf syntax to ping an address over
#the MGMT vrf from all hosts 
results = nr.run(task=ping_test)
print_result(results)
