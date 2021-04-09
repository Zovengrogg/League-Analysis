import pandas as pd
import requests

url = "https://canisback.com/matchId/matchlist_na1.json"
s = requests.get(url).content
# New match ID's
df1 = pd.read_json(s)

df1.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/newMatchId', index=False)
df1 = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/newMatchId')

# Current List of Match ID's
df2 = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/matchId')

if not df1.tail(100000).equals(df2):
    df2.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/matchId', mode='a', header=False, index=False)
    df2.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/KDA_Match_ID', mode='a', header=False, index=False)
    df2.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Win_Loss_Match_ID', mode='a', header=False, index=False)
    print('it wrked')




