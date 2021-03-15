import json
import csv
import requests


response = requests.get("https://ddragon.leagueoflegends.com/cdn/10.19.1/data/en_US/champion.json")
""""print(response.json())"""
champRawData = json.loads(response.text)
crd = champRawData['data']
"""print( crd ['Samira'])"""

Samira_stats = crd['Samira']['stats']
print(Samira_stats)

allchamps = []
allchamps =[["Name","Champ Id", "Base AD"]]
for i in crd:
    name = crd[i]['id']
    champId = crd[i]['key']
    ADbase = crd[i]['stats']['attackdamage']
    row =[name, champId, ADbase]
    allchamps.append(row)

print(allchamps)
for x in range(0, 3):
    print("We're on time %d" % (x))

with open("Champion_info", "w") as f:
    writer = csv.writer(f)
    writer.writerows(allchamps)