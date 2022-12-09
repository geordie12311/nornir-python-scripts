# Python script using Jinja2 template to send SNMP configuration from the host file based on platform type
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="config.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices

def snmp_template(task):
# above line is creating a function called snmp_tempate
    template = task.run(task=template_file, template="snmp.j2", path=f"{task.host.platform}-templates")
# above line is creating a variable called template and linking template to the template file snmp.j2 and providing the path to the file based on platform type
    task.host["snmp_config"] = template.result
# above line is going to bind the render template to a dictionary key and linking it to the results of template
    rendered = task.host["snmp_config"]
# above line is creating a new variable called rendered and making it equal to task host ospf_config
    configuration = rendered.splitlines()
# above line is going create the variable configuratoin, render the data and break it down line by line
    task.run(task=send_configs, configs=configuration)
# above line is going to use task.run to call send_configs and send the config from the configuration variable 

results = nr.run(task=snmp_template)
print_result(results)
# finally we are creating the variable results which is going to collate the results of the test_template function
# and print the results to screen
