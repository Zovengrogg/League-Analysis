import pandas as pd
import requests
import json
from riotwatcher import LolWatcher, ApiError

# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

api_key = 'RGAPI-dca7ad6f-ff5c-4ffb-8de7-01a601cb44a2'
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

df = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Data')


def editData(bWinLoss, bChamp, rChamp):
    # Red champ changes
    rData = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/%s' % rChamp)
    rData.iloc[1, bChamp] = rData.iloc[0, bChamp] + 1

    # Blue champ changes
    bData = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/%s' % bChamp)
    bData.iloc[1, bChamp] = bData.iloc[0, bChamp] + 1

    if bWinLoss == 1:
        bData.iloc[0, bChamp] = bData.iloc[0, bChamp] + 1
    else:
        rData.iloc[0, bChamp] = rData.iloc[0, bChamp] + 1

amount = 10
tail = df.tail(amount)

for i in range(amount):
    editData(tail.iloc[i]['Blue W/L'], champ_dict[str(tail.iloc[i]['Blue side champ'])], champ_dict[str(tail.iloc[i]['Red side champ'])])
    print(tail.iloc[i]['Blue side champ'])

