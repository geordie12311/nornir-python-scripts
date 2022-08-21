from ncclient import manager

m=manager.connect(host="sandbox-iosxe-latest-1.cisco.com", port="830", username="developer", password="C1sco12345", hostkey_verify=False,)
for capability in m.server_capabilities:
    print('*' * 50)
    print(capability)
config_template = open("/home/geordie/ios_config.xml").read()

netconf_config =config_template.format(interface_name="GigabitEthernet2", interface_description="testing netconf")
device_reply = m.edit_config(netconf_config, target="running")
print(device_reply)
