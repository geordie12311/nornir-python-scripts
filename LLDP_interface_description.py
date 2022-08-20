"""
Script to automatically add interface descriptions using LLDP
"""

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config

nr = InitNornir(config_file="config.yaml")


def lldp_map(task):
    r = task.run(task=netmiko_send_command, command_string = "show lldp neighbors", use_genie=True)
    task.host["facts"] = r.result
    outer = task.host["facts"]
    interfaces = outer['interfaces']
    for intf in interfaces:
        local_intf = intf
        remote_keys = interfaces[intf]['port_id'].keys()
        for key in remote_keys:
            remote_port = key
            remote_id_keys = interfaces[intf]['port_id'][key]['neighbors'].keys()
            for key in remote_id_keys:
                remote_id = key

        lldp_config = task.run(netmiko_send_config,name="Automating LLDP Network Descriptions",config_commands=[
            "interface " + str(local_intf),
            "description Connected to " + str(remote_id) + " via its " + str(remote_port) + " interface"]
        )


results = nr.run(task=lldp_map)
print_result(results)
