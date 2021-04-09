import csv
import time
from riotwatcher import LolWatcher, ApiError
import pandas as pd

# global variables
api_key = 'RGAPI-d6c5def9-86ea-4abd-a3fe-cbaa348749cc'
watcher = LolWatcher(api_key)
my_region = 'na1'

stats = []
# stats = [['W/L']]

amount = 50
for loop in range(5):
    # Uses match id's from csv
    matchId = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Win_Loss_Match_ID')
    tail = matchId.tail(amount)
    id = tail['0'].to_numpy()

    # For each match in my_matches
    for x in id:
        match_detail = watcher.match.by_id(my_region, x)
        # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
        if match_detail['gameMode'] == 'CLASSIC':
            if match_detail['teams'][0]['win'] == 'Fail':
                WinLoss = 'Blue Loss'
            else:
                WinLoss = 'Blue Win'
            stats.append(WinLoss)

    # Writes a CSV based on the stats array
    with open("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Win_Loss_Data", "a") as f:
        writer = csv.writer(f)
        writer.writerows(stats)

    matchId = matchId[:-amount]
    matchId.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/Win_Loss_Match_ID', index=False)

    # Forces wait time to help moderate API limited use
    time.sleep(120)
