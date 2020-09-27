import json
import os

class PlayersResult:
    
    def __init__(self, name, score, total):
        self.name = name
        self.score = score
        self.total = total


# Writes result to a text file            
def writeResult(winner, players):
    x = o = t = movesTotalwinnerO = movesTotalwinnerX =  0
    
    if not winner:
        t += 1
    elif winner.marker == "X":
        x += 1
        movesTotalwinnerX = winner.moves
    elif winner.marker == "O":
        o += 1
        movesTotalwinnerO = winner.moves

    movesTotal = players[0].moves + players[1].moves
    
    total = 1
    filename = "./slutuppgift/results.txt"
    try: 
        values = []
        with open(filename, "r") as a:
            for line in a:
                for value in line.split(": ")[1:]:
                    values.append(value.rstrip())
            
        data = open(filename, "w+")
        string = f'''---Games Statistics---

Total games: {int(values[0]) + total}
Total ties: {int(values[1]) + t} 
Total tie rate: {((int(values[1])+t)/(int(values[0])+total))*100}%
Total moves: {int(values[3]) + movesTotal} 

---X statistics
Total wins: {int(values[4]) + x} 
Winning rate: {((int(values[4])+x)/(int(values[0])+total))*100}% 
Total move winners: {int(values[6]) + movesTotalwinnerX} 

---O statistics
Total wins: {int(values[7]) + o} 
Winning rate: {((int(values[7])+o)/(int(values[0])+total))*100}% 
Total move winners: {int(values[9]) + movesTotalwinnerO} 
                '''
        data.write(string)
        data.close()
    
    #If file doesn't exist create new one
    except:
        data = open(filename, "w+")
        string = f'''---Games Statistics---
    
Total games: {total}
Total ties: {t} 
Total tie rate: {(t/total)*100}%
Total moves: {movesTotal} 

---X statistics
Total wins: {x} 
Winning rate: {(x/total)*100}% 
Total move winners: {movesTotalwinnerX} 

---O statistics
Total wins: {o} 
Winning rate: {(o/total)*100}% 
Total move winners: {movesTotalwinnerO} 
                '''
        data.write(string)
        print("Statistic file has been created in ", filename)
    
    for player in players:
        if player != winner.name:
            loser = player

    write_leaderboard(winner, loser)
    

#saves game into json file
def save_game(board, players, turn, filename):
    if not os.path.exists("./slutuppgift/saves"):
        try:
            os.mkdir("./slutuppgift/saves")
        except:
            print("something went wrong!")
            raise
    try:
        jstring = {
            "game": board.__dict__,
            "player1": players[0].__dict__,
            "player2": players[1].__dict__,
            "currentTurn": turn
        }
        json_file = open(f"./slutuppgift/saves/{filename}.json", "w+")
        json.dump(jstring, json_file)
        json_file.close()
    except:
        raise

#loads game from json file
def load_game(filename):
    json_file = open(f"./slutuppgift/saves/{filename}.json", "r")
    data = json.load(json_file)
    data_collection = data
    return data_collection
    
#updates leaderboard
#Not the cleanest code
def write_leaderboard(winner, loser):
    filename = "./slutuppgift/leaderboard.txt"
    score = total = 1

    if not os.path.exists(filename):
        data = open(filename, "w+")
        string = f'''---Leaderboard---
1,{winner.name},Wins,{score},Total games played,{total},Win rate,{(score/total)*100}%'''
        data.write(string)
        print("Created new leaderboard file")
        data.close()
    else:
        filename = "./slutuppgift/leaderboard.txt"
        try:
            
            values = []
            players = []
            data = open(filename, "r")

            for row in data:
                values.append(row.split(","))
            data.close()

            f = True
            for value in values:
                if f:
                    f = False
                    continue
                players.append(PlayersResult(value[1], int(value[3]), int(value[5])))
            
            currentPlayer = ""
            losingPlayer = ""

            for player in players:
                if player.name == winner.name:
                    currentPlayer = player
                elif player.name == loser.name:
                    losingPlayer = player

            
            if currentPlayer != "":
                currentPlayer.score += 1
                currentPlayer.total += 1
            else:
                players.append(PlayersResult(winner.name, 1, 1))
            
            if losingPlayer != "":
                losingPlayer.total += 1
            else:
                players.append(PlayersResult(loser.name, 0, 1))

            players.sort(key=lambda x: x.score, reverse=True)
            
            data = open(filename, "w+")
            string = "---Leaderboard---\n"
            for player in players:
                string += f"{players.index(player)+1},{player.name},Wins,{player.score},Total games played,{player.total},Win rate,{(player.score/player.total)*100}%\n"

            data.write(string)
            data.close()

        except:
            print("Error")
            raise


def load_statistics():
    result = []
    values = []
    filename = "./slutuppgift/results.txt"
    
    data = open(filename, "r")

    print(data.read())

    print("---------Leaderboard----------")

    filename = "./slutuppgift/leaderboard.txt"
    
    data = open(filename, "r")
    for row in data:
        values.append(row.split(","))
    data.close()

    f = True
    for value in values:
        if f:
            f = False
            continue
        print(f'''{value[0]}: {value[1]} 
Total games won: {value[3]} 
Total games played: {value[5]}
Game rate: {value[7]}
''')
    

