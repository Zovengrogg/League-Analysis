import time
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv

# This program gathers the data for duo matchups and puts them into a CSV

# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

api_key = 'RGAPI-cdc16730-d409-4d4e-9898-2910a9dbec51'
watcher = LolWatcher(api_key)
my_region = 'na1'


amount = 30
# matchId = matchId[:-10]
for loop in range(30):
    matchId = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/DLM_Match_ID')
    stats = []
    # stats = [['Blue W/L', 'Blue Side Supp', 'Blue Side Adc', 'Red Side Supp', 'Red Side Adc']]
    # Uses match id's from csv
    tail = matchId.tail(amount)
    id = tail['0'].to_numpy()
    start = time.time()
    # For each match in my_matches
    count = 0
    for x in id:
        print(x)
        time.sleep(3)
        match_detail = watcher.match.by_id(my_region, x)
        # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
        if match_detail['gameMode'] == 'CLASSIC':
            i = 4
            for participant in match_detail['participants']:
                # checks role of participant
                role = participant['timeline']['role']
                lane = participant['timeline']['lane']
                if role == 'DUO_CARRY' and (lane == 'BOTTOM' or lane == 'TOP'):
                    i -= 1
                    partId = participant['participantId']
                    partStats = match_detail['participants'][partId - 1]
                    if partStats['teamId'] == 100:
                        bChampAdc = partStats['championId']
                        tf = partStats['stats']['win']
                        if tf:
                            bWinLoss = 1
                        else:
                            bWinLoss = 0
                    else:
                        rChampAdc = partStats['championId']
                if role == 'DUO_SUPPORT' and (lane == 'BOTTOM' or lane == 'TOP'):
                    i -= 1
                    partId = participant['participantId']
                    partStats = match_detail['participants'][partId - 1]
                    if partStats['teamId'] == 100:
                        bChampSupp = partStats['championId']
                        tf = partStats['stats']['win']
                        if tf:
                            bWinLoss = 1
                        else:
                            bWinLoss = 0
                    else:
                        rChampSupp = partStats['championId']
            if i != 0:
                continue
            # b = Blue side, r = Red side
            row = [bWinLoss, bChampSupp, bChampAdc, rChampSupp, rChampAdc]
            stats.append(row)

    end = time.time()-start
    print('Loop '+loop+': ', end)

    # Writes a CSV based on the stats array
    with open("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/DLM_Data.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(stats)

    # Removes last 'amount' rows and rewrites the file
    matchId = matchId[:-amount]
    matchId.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/DLM_Match_ID', index=False)
    # Forces wait time to help moderate API limited use
    time.sleep(30)



