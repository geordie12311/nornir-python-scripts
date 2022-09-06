# Python script that will load variables from host specific var files held in host_vars,
# use a Jinja2 template to send OSPF configuration from those host specific files to the hosts
import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml

nr = InitNornir(config_file="config1.yaml")
#The above line is telling nornir where the config file is located
user = input("Enter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices

def load_vars(task):
# above line is creating a function called load_vars
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
# above line is creating a variable called data and linking it to the host specific yaml files in host_vars folder
    task.host["facts"] = data.result
# above line is going to bine the render template to a dictionayr key called facts and link it to the results of data
    ospf_template(task)
# above line is going to call the function ospf_templates below

def ospf_template(task):
# above line is creating a function called ospf_tempate
    template = task.run(task=template_file, template="ospf_vars.j2", path=f"{task.host.platform}-templates")
# above line is creating a variable called template and linking template to the template file sw-ospf.j2 and providing the path to the file
    task.host["ospf_config"] = template.result
# above line is going to bind the render template to a dictionary key and linking it to the results of template
    rendered = task.host["ospf_config"]
# above line is creating a new variable called rendered and making it equal to task host ospf_config
    configuration = rendered.splitlines()
# above line is going create the variable configuratoin, render the data and break it down line by line
    task.run(task=send_configs, configs=configuration)
# above line is going to use task.run to call send_configs and send the config from the configuration variable 

results = nr.run(task=load_vars)
print_result(results)
# finally we are creating the variable results which is going to collate the results of the test_template function
# and print the results to screen
