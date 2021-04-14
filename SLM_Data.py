import time
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv

# 20 requests every 1 seconds(s)
# 100 requests every 2 minutes(s)

api_key = 'RGAPI-b780b87f-3665-4a1e-a4c6-45ccd8a8663e'
watcher = LolWatcher(api_key)
my_region = 'na1'

stats = []
statsTop = []
# statsTop = [['Blue W/L', 'Blue side champ', 'Red side champ', 'Role']]
statsJg = []
# statsJg = [['Blue W/L', 'Blue side champ', 'Red side champ', 'Role']]

amount = 30
matchId = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Match_ID')
# matchId = matchId[:-10]
for loop in range(10):
    # Uses match id's from csv
    tail = matchId.tail(amount)
    id = tail['0'].to_numpy()
    start = time.time()

    # For each match in my_matches
    for x in id:
        time.sleep(3)
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
            if not middle:
                continue
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
    print('Middle Loop: ', end)

    # Writes a CSV based on the stats array
    with open("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Data", "a") as f:
        writer = csv.writer(f)
        writer.writerows(stats)

    time.sleep(60)

    for x in id:
        time.sleep(3)
        match_detail = watcher.match.by_id(my_region, x)
        # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
        if match_detail['gameMode'] == 'CLASSIC':
            i = 0
            top = []
            for participant in match_detail['participants']:
                # checks role of participant
                role = participant['timeline']['role']
                lane = participant['timeline']['lane']
                if role == 'SOLO' and (lane == 'TOP' or 'BOTTOM'):
                    partId = participant['participantId']
                    top.append(partId)
                i += 1
            if not top:
                continue
            for y in top:
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
            row = [bWinLoss, bChamp, rChamp, 'Top']
            statsTop.append(row)

    end = time.time()-start
    print('Top Loop: ', end)

    # Writes a CSV based on the stats array
    with open("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Data", "a") as f:
        writer = csv.writer(f)
        writer.writerows(statsTop)

    time.sleep(60)

    for x in id:
        time.sleep(3)
        match_detail = watcher.match.by_id(my_region, x)
        # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
        if match_detail['gameMode'] == 'CLASSIC':
            i = 0
            jg = []
            for participant in match_detail['participants']:
                # checks role of participant
                role = participant['timeline']['role']
                lane = participant['timeline']['lane']
                if role == 'NONE' and lane == 'JUNGLE':
                    partId = participant['participantId']
                    jg.append(partId)
                i += 1
            if not jg:
                continue
            for y in jg:
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
            row = [bWinLoss, bChamp, rChamp, 'Jungle']
            statsJg.append(row)

    end = time.time()-start
    print('Jg Loop: ', end)

    # Writes a CSV based on the stats array
    with open("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Data", "a") as f:
        writer = csv.writer(f)
        writer.writerows(statsJg)

    # Removes last 'amount' rows and rewrites the file
    matchId = matchId[:-amount]
    matchId.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/SLM_Match_ID', index=False)

    # Forces wait time to help moderate API limited use
    time.sleep(30)



