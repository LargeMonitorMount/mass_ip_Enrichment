import http.client
import json
import csv

def asd (ip):
    conn = http.client.HTTPSConnection("rest.db.ripe.net")
    payload = ''
    headers = {}
    conn.request("GET", "/search.json?query-string="+ip, payload, headers)
    res = conn.getresponse()
    data = res.read()

    x = json.loads(data.decode("utf-8"))

    intenum_netname = ""
    intenum_descr = ""
    route_netname = ""
    
    
    
    for a in x["objects"]["object"]:
        if a["type"] == "inetnum":
            for b in a["attributes"]["attribute"]:
                if b["name"] == "netname":
                    netname = b["value"]
                if b["name"] == "descr":
                    descr = b["value"]

    return netname, descr

l = csv.writer(open("output.csv", 'w', newline=''))
#header.
l.writerow(["ip","decr","netname"])

with open("input.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line


 
for a in content:
    asdf = asd(a)
    l.writerow ([a,asdf[1],asdf[0]])