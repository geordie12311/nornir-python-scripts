import xmltodict

#Get the XML file data
stream = open('sample.xml','r')

#Parse the XML file into an Ordered Dict
xml = xmltodict.parse(stream.read())

for e in xml["People"]["Person"]:
    print(e)