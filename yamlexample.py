import yaml
from yaml import load, load_all

stream = open('sample.yaml','r')
documents = load_all(stream, Loader=yaml.FullLoader)

#print(type(documents))

for doc in documents:
    #print(type(doc))
    print(doc['people'][0]['Email'])
    print(doc['people'][1]['Email'])
    print(doc['people'][2]['Email'])