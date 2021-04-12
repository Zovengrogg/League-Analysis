import time
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv

# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

api_key = 'RGAPI-dca7ad6f-ff5c-4ffb-8de7-01a601cb44a2'
watcher = LolWatcher(api_key)
my_region = 'na1'

stats = []
# stats = [['Blue W/L', 'Blue side champ', 'Red side champ', 'Role']]
amount = 50
matchId = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Match_ID')
for loop in range(5):
    # Uses match id's from csv
    tail = matchId.tail(amount)
    id = tail['0'].to_numpy()
    start = time.time()

    # For each match in my_matches
    for x in id:
        match_detail = watcher.match.by_id(my_region, x)
        # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
        if match_detail['gameMode'] == 'CLASSIC':
            i = 0
            middle = []
            for participant in match_detail['participants']:
                # checks role of participant
                role = participant['timeline']['role']
                lane = participant['timeline']['lane']
                if role == 'SOLO' and lane == 'MIDDLE':
                    partId = participant['participantId']
                    middle.append(partId)
                i += 1
            for y in middle:
                partStats = match_detail['participants'][y - 1]
                if partStats['teamId'] == 100:
                    bChamp = partStats['championId']
                    tf = partStats['stats']['win']
                    if tf:
                        bWinLoss = 1
                    else:
                        bWinLoss = 0
                else:
                    rChamp = partStats['championId']
            # b = Blue side, r = Red side
            row = [bWinLoss, bChamp, rChamp, 'Middle']
            stats.append(row)

    end = time.time()-start
    print('Loop: ', end)

    # Writes a CSV based on the stats array
    with open("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Data", "w") as f:
        writer = csv.writer(f)
        writer.writerows(stats)

    # Removes last 'amount' rows and rewrites the file
    matchId = matchId[:-amount]
    matchId.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Match_ID', index=False)

    # Forces wait time to help moderate API limited use
    time.sleep(120)



