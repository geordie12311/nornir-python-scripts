#simple python script using nornir_scrapli to send a show command to hosts
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

results = nr = nr.run(task=send_command, command="show version")
print_result(results)
