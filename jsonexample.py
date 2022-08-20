import json

jsonstr = """{"people":[{"Id":"1","FirstName":"Geordie","LastName":"Harwood",
    "Email":"geordie123@gmail.com"},{"Id":"2","FirstName":"Elaine","LastName":"Harwood",
    "Email":"elaine123@gmail.com"},{"Id":"3","FirstName":"Jack","LastName":"Harwood",
    "Email":"jack123@gmail.com"}]}"""

jsonobj = json.loads(jsonstr)

print(jsonobj['people'][1])

jsonobj = json.load(open('sample.json'))

print(jsonobj['people'])