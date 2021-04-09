import json
import csv
import requests


response = requests.get("https://ddragon.leagueoflegends.com/cdn/10.19.1/data/en_US/champion.json")
""""print(response.json())"""
champRawData = json.loads(response.text)
crd = champRawData['data']
"""print( crd ['Samira'])"""

# Samira_stats = crd['Samira']['stats']

allchamps = []
allchamps =[["Name", "Champ Id"]]
for i in crd:
    name = crd[i]['id']
    champId = crd[i]['key']
    row =[name, champId]
    allchamps.append(row)

print(allchamps)
for x in range(0, 3):
    print("We're on time %d" % (x))

with open("Champion_info", "w") as f:
    writer = csv.writer(f)
    writer.writerows(allchamps)