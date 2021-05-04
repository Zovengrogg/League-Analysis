import pandas as pd
import requests

# This program fetches match ID's from a website and puts those ID's into separate CSV's for other programs to use

url = "https://canisback.com/matchId/matchlist_na1.json"
s = requests.get(url).content
# New match ID's
df1 = pd.read_json(s)

df1.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/newMatchId', index=False)
df1 = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/newMatchId')

# Current List of Match ID's
df2 = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/matchId')
tail1 = df1.tail(10).reset_index()
tail2 = df2.tail(10).reset_index()

if not tail1['0'].equals(tail2['0']):
    df1.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/matchId', mode='a', header=False, index=False)
    df1.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/KDA_Match_ID', mode='a', header=False, index=False)
    df1.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Win_Loss_Match_ID', mode='a', header=False, index=False)
    df1.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Match_ID', mode='a', header=False, index=False)
    df1.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/DLM_Match_ID', mode='a', header=False, index=False)
    print('it wrked')

