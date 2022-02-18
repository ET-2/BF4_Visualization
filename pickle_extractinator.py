import pickle
import json

file = open("game_data.obj", "rb")
obj = pickle.load(file)

#JSON for win/loss stats
win_loss = {
    'total': 0,
    'wins': 0,
    'losses': 0 
}

win_loss['total'] = len(obj)

#JSON for games and player data
games = {}
count = 0

for i in obj:

    count += 1
    temp_games = {}
    temp_winners = []
    temp_losers = []

    if i.win_loss == "WON":
        win_loss['wins'] += 1

    if i.win_loss == "LOST":
        win_loss['losses'] += 1

    temp_games["ID"] = i.game_id
    temp_games["win_loss"] = i.win_loss

    for p in i.winners:
        
        temp_player = {}

        temp_player["name"] = p.name
        temp_player["player_ID"] = p.player_ID
        temp_player["game_ID"] = p.game_ID
        temp_player["position"] = p.position
        temp_player["kills"] = p.kills
        temp_player["deaths"] = p.deaths
        temp_player["score"] = p.score

        temp_winners.append(temp_player)
    
    for p in i.losers:
        
        temp_player = {}

        temp_player["name"] = p.name
        temp_player["player_ID"] = p.player_ID
        temp_player["game_ID"] = p.game_ID
        temp_player["position"] = p.position
        temp_player["kills"] = p.kills
        temp_player["deaths"] = p.deaths
        temp_player["score"] = p.score

        temp_losers.append(temp_player)

    temp_games["winners"] = temp_winners
    temp_games["losers"] = temp_losers
    games[count] = temp_games

with open("win_loss.json", "w") as outfile:
    json.dump(win_loss, outfile)

with open("game_data.json", "w") as outfile:
    json.dump(games, outfile)