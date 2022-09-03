from nornir import InitNornir
from nornir_scrapli.tasks import send_config
from nornir_utils.plugins.functions import print_result

<<<<<<< HEAD
nr = InitNornir(config_file="config.yaml")
=======
nr =InitNornir(config_file="config.yaml")
>>>>>>> b9a12a3953530a6658704acc9f2a0fed66d89c0c

def random_config(task):
    task.run(task=send_config, config=f"ntp server {task.host['ntp_server']}")

results = nr.run(task=random_config)
print_result(results)
