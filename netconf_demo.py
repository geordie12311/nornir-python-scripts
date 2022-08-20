import xmltodict
import xml.dom.minidom
import pprint
from ncclient import manager

router = {"host": "10.10.10.1", "port": "830", "username": "cisco", "password": "cisco123"}
print(router["host"])
print(router["port"])
print(router["username"])
print(router["password"])

netconf_filter = """
<filter>
 <interfaces xmls="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interfaces>
   <name>GigabitEthernet1</name>
  </interface>
 </interface>
</filter>
"""
