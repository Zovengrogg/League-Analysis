import pandas as pd
import requests
import json
from riotwatcher import LolWatcher, ApiError

# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

api_key = 'RGAPI-cdc16730-d409-4d4e-9898-2910a9dbec51'
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


df1 = pd.read_csv("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/DLM_Data")
df2 = pd.read_csv("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/DLM_Data")
df1 = df1.sort_values(by=['Blue Side Supp', 'Blue Side Adc'])
df2 = df2.sort_values(by=['Red Side Supp', 'Red Side Adc'])

