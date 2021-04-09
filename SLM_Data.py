import json

import requests
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv

api_key = 'RGAPI-b5fc2381-e81a-45ea-9cf5-d41a2239826b'
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