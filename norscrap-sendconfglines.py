from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
#importing send_configs from nornir_scrapli to send a configuration change
nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located

def send_configs_test(task):
    task.run(task=send_configs, configs=["router ospf 1", "network 0.0.0.0 255.255.255.255 area 1"])
#above function is going to use the send_configs to send a list of configuration commands

results = nr.run(task=send_configs_test)
#above line is setting an object results that is aligned to the task output
print_result(results)
