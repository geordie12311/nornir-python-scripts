import getpass
import time
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from rich import print as rprint

rprint("[bold red on yellow]*****THIS SCRIPT WILL RUN 'SHOW RUN' COMMAND AND DISPLAY THE OUTPUT FROM ALL HOSTS*****[/bold red on yellow]")
#displaying a banner to confirm what the script does to the use
nr = InitNornir(config_file="config1.yaml")

password = getpass.getpass()
nr.inventory.defaults.password = password

results = nr = nr.run(task=send_command, command="show run")
print_result(results)
