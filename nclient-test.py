from ncclient import manager
import xml.dom.minidom
from pprint import pprint
import xmltodict

router = {"host": "sandbox-iosxe-latest-1.cisco.com", "port": "830", "username": "developer", "password": "C1sco12345"}

netconf_filter = """
<filter>
  <interfaces xmls="urn:ietf:params:xml:yang:ietf-interfaces">
    <interface>
        <name>GigatbitEthernet2</name> 
    </interface>
  </interfaces>
  <interfaces-state xmls="urn:ietf:params:xml:yang:ietf-interfaces">
    <interface>
        <name>GigatbitEthernet2</name>
    </interface>
  </interfaces-state>
</filter>
 
"""

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
    for capability in m.server_capabilities:
        print('*' * 50)
        print(capability)

#        print('connected')
        interface_netconf = m.get(netconf_filter)
        xmlDom = xml.dom.minidom.parseString(str(interface_netconf))
        print(xmlDom.topretty.xml(indent= " "))
        print('*' * 25 + 'Break' + '*' * 50)
#        print("getting running config")
    
#    interface_python = xmltodict.parse(interface_netconf.xml)[
#        "rpc-reply"]["data"]
#    pprint(interface_python)
#    name = interface_python['interfaces']['interface']['name']['#text']
#    print(name)
    
#    config = interface_python["interfaces"]["interface"]
#    op_state = interface_python["interfaces-state"]["interface"]
    
#    print("Start")
#    print(f"Name: {config['name']['#text']}")
#    print(f"description {config['description']}")
#    print(f"Packets in {op_state['statistics']}")

    #m.close_session()
