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


def editData(bWinLoss, bChamp, rChamp):
    # Red champ changes
    rData = pd.read_csv(
        '/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Champ Matchups/%s' % rChamp).set_index('Data')
    rData.loc['Total Games', bChamp] = rData.loc['Total Games', bChamp] + 1

    # Blue champ changes
    bData = pd.read_csv(
        '/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Champ Matchups/%s' % bChamp).set_index('Data')
    bData.loc['Total Games', rChamp] = bData.loc['Total Games', rChamp] + 1

    if bWinLoss == 1:
        bData.loc['Wins', rChamp] = bData.loc['Wins', rChamp] + 1
    else:
        rData.loc['Wins', bChamp] = rData.loc['Wins', bChamp] + 1

    rData.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Champ Matchups/%s' % rChamp)
    bData.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Champ Matchups/%s' % bChamp)


df = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Data')
for i in range(len(df.index)):
    editData(df.iloc[i]['Blue W/L'], champ_dict[str(df.iloc[i]['Blue side champ'])],
             champ_dict[str(df.iloc[i]['Red side champ'])])

df = df.iloc[0:0]
df.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Data', index=False)
