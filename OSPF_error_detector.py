"""
Automated test to check OSPF links share the same network/mask, area and timers.
Be aware that as CDP is used you will see the mismatch from both traffic directions 
ie: it will show a failure from R1 to R2, as well as R2 back to R1.
This is the same mismatch shown from both perspectives of each device.
This script uses CDP and was designed to operate between directly connected, OSPF-enabled devices.
Switched shared segments will break the CDP logic. 
This script uses Nornir2, not Nornir3. Install with: pip3 install nornir"<3"
"""

import os
import ipaddress
from collections import defaultdict
import requests
from nornir import InitNornir
from nornir.plugins.tasks.apis import http_method
from rich import print as rprint

nr = InitNornir(config_file="config.yaml")
requests.packages.urllib3.disable_warnings()

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

CLEAR = "clear"
os.system(CLEAR)
config_dict = defaultdict(dict)
facts_dict = defaultdict(dict)
network_error = []
area_error = []
timer_error = []

rprint("[cyan]SCANNING...[/cyan]\n\n")


def get_ospf(task):
    """
    Use RESTCONF to retrieve data and create 2 dictionaries of OSPF info
    """
    send = task.run(
        http_method,
        auth=("john", "cisco"),
        verify=False,
        method="get",
        headers=headers,
        url=f"https://{task.host.hostname}:443/restconf/data/ospf-oper-data",
    )

    sender = task.run(
        http_method,
        auth=("john", "cisco"),
        verify=False,
        method="get",
        headers=headers,
        url=f"https://{task.host.hostname}:443/restconf/data/native/interface",
    )
    task.host["ospf-facts"] = send.response.json()
    task.host["ospf-config"] = sender.response.json()

    config_interfaces = task.host["ospf-config"]["Cisco-IOS-XE-native:interface"]
    for inter_types in config_interfaces:
        interfaces = config_interfaces[inter_types]
        for intf in interfaces:
            try:
                name = intf["name"]
                intlink = inter_types + str(name)
                ip = intf["ip"]["address"]["primary"]["address"]
                mask = intf["ip"]["address"]["primary"]["mask"]
                config_dict[f"{task.host}"][intlink] = [ip, mask]
            except KeyError:
                pass

    instances = task.host["ospf-facts"]["Cisco-IOS-XE-ospf-oper:ospf-oper-data"][
        "ospf-state"
    ]["ospf-instance"]
    for instance in instances:
        areas = instance["ospf-area"]
        for area in areas:
            try:
                area_id = area["area-id"]
                ospf_interfaces = area["ospf-interface"]
                for ospf_interface in ospf_interfaces:
                    name = ospf_interface["name"]
                    dead = ospf_interface["dead-interval"]
                    hello = ospf_interface["hello-interval"]
                    facts_dict[f"{task.host}"][name] = [dead, hello, area_id]
            except KeyError:
                pass


def get_cdp(task):
    """
    Use CDP to correlate connected links.
    Pull link infomation from OSPF dictionaries and test
    """
    send = task.run(
        http_method,
        auth=("john", "cisco"),
        verify=False,
        method="get",
        headers=headers,
        url=f"https://{task.host.hostname}:443/restconf/data/cdp-neighbor-details",
    )
    task.host["cdp-facts"] = send.response.json()
    cdp_neighbors = task.host["cdp-facts"][
        "Cisco-IOS-XE-cdp-oper:cdp-neighbor-details"
    ]["cdp-neighbor-detail"]
    for neighbor in cdp_neighbors:
        dev_name = neighbor["device-name"]
        local_intf = neighbor["local-intf-name"]
        port_id = neighbor["port-id"]

        if local_intf.startswith("Gi"):
            local_ip = config_dict[f"{task.host}"][local_intf][0]
            local_mask = config_dict[f"{task.host}"][local_intf][1]
            local_net = ipaddress.ip_network(local_ip + "/" + local_mask, strict=False)
            remote_ip = config_dict[dev_name][port_id][0]
            remote_mask = config_dict[dev_name][port_id][1]
            remote_net = ipaddress.ip_network(
                remote_ip + "/" + remote_mask, strict=False
            )
            local_area = facts_dict[f"{task.host}"][local_intf][2]
            remote_area = facts_dict[dev_name][port_id][2]
            local_hello = facts_dict[f"{task.host}"][local_intf][1]
            remote_hello = facts_dict[dev_name][port_id][1]
            local_dead = facts_dict[f"{task.host}"][local_intf][0]
            remote_dead = facts_dict[dev_name][port_id][0]
            if not local_net == remote_net:
                network_error.append(
                    (
                        f"NETWORK MISMATCH: {task.host} {local_intf} {local_net}"
                        f" ~ ~ {dev_name} {port_id} {remote_net}"
                    )
                )
            if not local_area == remote_area:
                area_error.append(
                    (
                        f"AREA MISMATCH: {task.host} {local_intf} area {local_area}"
                        f" ~ ~ {dev_name} {port_id} area {remote_area}"
                    )
                )
            if not local_hello == remote_hello:
                timer_error.append(
                    (
                        f"TIMER MISMATCH: {task.host} {local_intf} hello interval {local_hello}"
                        f" ~ ~ {dev_name} {port_id} hello interval {remote_hello}"
                    )
                )
            if not local_dead == remote_dead:
                timer_error.append(
                    (
                        f"TIMER MISMATCH: {task.host} {local_intf} dead interval {local_dead}"
                        f" ~ ~ {dev_name} {port_id} dead interval {remote_dead}"
                    )
                )


ospf_result = nr.run(task=get_ospf)
cdp_result = nr.run(task=get_cdp)
if network_error:
    network_fails = sorted(network_error)
    rprint(network_fails)
if area_error:
    area_fails = sorted(area_error)
    rprint(area_fails)
if timer_error:
    timer_fails = sorted(timer_error)
    rprint(timer_fails)

rprint("\n[yellow]*** SCAN COMPLETED *************[/yellow]\n")
