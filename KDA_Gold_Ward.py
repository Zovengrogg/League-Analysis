import time
from riotwatcher import LolWatcher, ApiError
import json
import csv
import requests
import urllib.request

url = "https://canisback.com/matchId/matchlist_na1.json"
contents = urllib.request.urlopen(url).read()
matchId = eval(contents)

# global variables
api_key = 'RGAPI-be7187ea-a4cc-4284-a598-082cf84142f5'
watcher = LolWatcher(api_key)
my_region = 'na1'
# Ddragon
response = requests.get("https://ddragon.leagueoflegends.com/cdn/10.19.1/data/en_US/champion.json")
champRawData = json.loads(response.text)
crd = champRawData['data']

# check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

# champ static list data to dict for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

stats = [['W/L', 'Kills', 'Deaths', 'Assists', 'Gold', 'Time', 'Vision Score']]

# Uses match id's from json
id = []
for y in range(1):
    id.append(matchId[y])

# For each match in my_matches
for x in id:
    match_detail = watcher.match.by_id(my_region, x)
    # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
    if match_detail['gameMode'] == 'CLASSIC':
        print(match_detail['participants'][0])

        time = match_detail['gameDuration']
print(stats)
# Writes a CSV based on the stats array
# with open("data1", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(stats)
