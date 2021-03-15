import time
from riotwatcher import LolWatcher, ApiError
import json
import requests
import urllib.request

url = "https://canisback.com/matchId/matchlist_na1.json"
contents = urllib.request.urlopen(url).read()
matchId = eval(contents)

# global variables
summoner = 'Zovengrogg'
api_key = 'RGAPI-d6a181b5-c5f6-4260-8331-1ae7ded7799f'
watcher = LolWatcher(api_key)
my_region = 'na1'
# Ddragon
response = requests.get("https://ddragon.leagueoflegends.com/cdn/10.19.1/data/en_US/champion.json")
champRawData = json.loads(response.text)
crd = champRawData['data']

# Gets info on summoner
me = watcher.summoner.by_name(my_region, summoner)

# check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

# champ static list data to dict for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

stats = [['W/L']]

# Uses match id's from json
id = []
for y in range(10):
    id.append(matchId[y])

# For each match in my_matches
for x in id:
    start = time.time()
    match_detail = watcher.match.by_id(my_region, x)
    # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
    if match_detail['gameMode'] == 'CLASSIC':
        if match_detail['teams'][0]['win'] == 'Fail':
            WinLoss = 'Loss'
        else:
            WinLoss = 'Win'
        stats.append(WinLoss)
    finish = time.time() - start
    print('Looped after: ', finish)
print(stats)
# Writes a CSV based on the stats array
# with open("data1", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(stats)
