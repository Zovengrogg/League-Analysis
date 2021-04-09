import time
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import csv

# global variables
api_key = 'RGAPI-d6c5def9-86ea-4abd-a3fe-cbaa348749cc'
watcher = LolWatcher(api_key)
my_region = 'na1'

stats = []
# stats = [['W/L', 'Kills', 'Deaths', 'Assists', 'Gold', 'Time', 'Vision Score', 'Role']]
amount = 50
for loop in range(5):
    # Uses match id's from csv
    matchId = pd.read_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/KDA_Match_ID')
    tail = matchId.tail(amount)
    id = tail['0'].to_numpy()
    start = time.time()

    # For each match in my_matches
    for x in id:
        match_detail = watcher.match.by_id(my_region, x)
        # checks to see if game is summnoner's rift. Can use same logic for ranked solo or ranked 5v5
        if match_detail['gameMode'] == 'CLASSIC':
            i = 0
            for participant in match_detail['participants']:
                # checks role of participant
                role = participant['timeline']['role']
                if role == 'DUO_CARRY':
                    partId = participant['participantId']
                    partStats = match_detail['participants'][partId - 1]
                    tf = partStats['stats']['win']
                    if tf:
                        winLoss = 1
                    else:
                        winLoss = 0
                    kills = partStats['stats']['kills']
                    deaths = partStats['stats']['deaths']
                    assists = partStats['stats']['assists']
                    visionScore = partStats['stats']['visionScore']
                    gold = partStats['stats']['goldEarned']
                    gameTime = match_detail['gameDuration']
                    # Detailed vision score
                    wardsBought = partStats['stats']['visionWardsBoughtInGame']
                    wardsPlaced = partStats['stats']['wardsPlaced']
                    wardsKilled = partStats['stats']['wardsKilled']
                    row = [winLoss, kills, deaths, assists, gold, gameTime, visionScore, role]
                    stats.append(row)
                i += 1
    end = time.time()-start
    print('Loop: ', end)

    # Writes a CSV based on the stats array
    with open("/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/KDA_Data", "a") as f:
        writer = csv.writer(f)
        writer.writerows(stats)

    # Removes last 50 rows and rewrites the file
    matchId = matchId[:-amount]
    matchId.to_csv('/Users/mitchel/Documents/Projects/League-Analysis/CSV Data/KDA_Match_ID', index=False)

    # Forces wait time to help moderate API limited use
    time.sleep(120)
