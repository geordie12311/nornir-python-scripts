#python script using netmiko plugin send_config to send configuration
#from a text file "randomconfig.txt"
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
#importing netmiko send_config library

nr = InitNornir(config_file="config.yaml")

def send_config_test(task):
    task.run(task=netmiko_send_config, config_file="netmiko-randomconfig.txt")
#function is sending the configuration commands in the file to the hosts
results = nr.run(task=send_config_test)
print_result(results)
#setting the object results to output of the send_config_test function
