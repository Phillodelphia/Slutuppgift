from filewriter import writeResult, load_game, save_game, load_statistics
from random import randrange
import os

#Board class is where the program builds new boards stored in a board_grid list
class Board:
    def __init__ (self, rule, width, height):
        self.width = width
        self.height = height
        self.rule = rule
        self.board_grid = []


    # Create board with width and height
    def create_board (self):
        for i in range(0, self.height):
            temporary = []
        
            for j in range(0, self.width):
        
                temporary.append("-")
            self.board_grid.append(temporary)
        
        
        return self.board_grid
    
    #prints the board
    def printBoard(self):
        
        print("".ljust(4), " ".join(str(i).rjust(4) for i in range(1, len(self.board_grid[0])+1)))

        for i, y in enumerate(self.board_grid):
            print(f"{str(i+1).ljust(5)} {y}")
        
            

    # Checks if 2 cordinates is inside the list
    def check_bound(self, x, y):
        if y > len(self.board_grid)-1 or y < 0 or x > len(self.board_grid[0])-1 or x < 0:
            return True
        else:
            return False
    
    # checks the cordinates inputed if the cordinates are valid
    def place_marker(self, currentPlayer, x, y):
        if self.check_bound(x, y):
                print("Not valid cordinate")
                return False
        elif self.board_grid[y][x] != "-":
            print("Something blocking this cordinate")
            return False
        else:
            self.board_grid[y][x] = currentPlayer.marker
            currentPlayer.moves += 1
            return True
    
    #Checks if one of the players have won the game
    def check_win(self, currentPlayer, x, y, diffX, diffY):
        counter = 0

        #Steps backwards until the selector has hit a wall
        while not self.check_bound((x+-diffX), (y+-diffY)) and x != 0 and y != 0:
            x = x + -diffX
            y = y + -diffY

        #Once on the back of the board step forwards and see if the win condition is met until it hits a wall again
        for i in range(len(self.board_grid)):
            if self.check_bound(x, y):
                break 
            if self.board_grid[y][x] == currentPlayer.marker:
                counter += 1
            else:
                counter = 0

            #if the win condition is true make the player win
            if counter == self.rule:
                currentPlayer.win = True
                self.printBoard()
                print(f"{currentPlayer.name} with {currentPlayer.marker} has won this round game")
    
                writeResult(currentPlayer, players)
                return True
            
            x += diffX
            y += diffY


    
    #https://stackoverflow.com/questions/398299/looping-in-a-spiral/1555236
    #Searches for any markers nearby the current placed one
    def search_markers(self, currentPlayer, xCor, yCor):
        Y = X = 3
        x = y = 0
        dx = 0
        dy = -1
        for i in range(max(X, Y)**2):
            if (-X/2 < x <= X/2) and (-Y/2 < y <= Y/2):
                newX = x+xCor
                newY = y+yCor
                #print (f"X: {newX}, Y: {newY}")

                if not self.check_bound(x+xCor, y+yCor) and self.board_grid[newY][newX] == currentPlayer.marker:
                    #take current mark position - new marker to get the direction it needs to search
                    diffX = newX - xCor
                    diffY = newY - yCor
                    #checks so that the difference isn't 0 meaning the program accidently choose the same marker twice
                    if diffX != 0 or diffY != 0: 
                        if self.check_win(currentPlayer, xCor, yCor, diffX, diffY):
                            break

            
            if x == y or (x < 0 and x == -y) or (x > 0 and x == 1-y):
                dx, dy = -dy, dx
            x, y = x+dx, y+dy
        

            
#Player class is where the program build players or bots       
class Player:

    def __init__(self, name, marker):
        self.name = name
        self.marker = marker
        self.moves = 0
        self.typeP = "human"
        self.win = False

    #Randomizes a coordinate that's valid
    def randomize_position(self, board):
        cord = [randrange(1, len(board.board_grid)+1), randrange(1, len(board.board_grid[0])+1)]
        while not board.board_grid[cord[1]-1][cord[0]-1] == '-':
            cord = [randrange(1, len(board.board_grid)+1), randrange(1, len(board.board_grid[0])+1)]
        
        return cord
    

players = []

# switches player turn
def switch_turn (turn):
    
    if turn:
        return players[1]
    else:
        return players[0]

# starts a game either progressed or a new game
def play_game(board, turn):
    
    currentPlayer = players[0]

    turnC = 0
    print(f'''
---How to play---
Type a x and y axis to put a marker on the board and try to get {board.rule} in a row.

To save a game type "save" and then enter save file name

You can quit anytime by typing "quit"    
    ''')

    #game loops until someone has won
    while not players[0].win or not players[1].win:
        
        board.printBoard()
        currentPlayer = switch_turn(turn)
        print(f"{currentPlayer.name}'s turn\n")
        try:
            #If the player is a robot make them randomize a coordinate
            if currentPlayer.typeP == "robot":

                checkcorr = currentPlayer.randomize_position(board)
                
                playerInput = f"{checkcorr[0]} {checkcorr[1]}"
                
            else:
                playerInput = input("Where do you want to place your marker? Input X and Y cordinates (x y) remember to use space")

            #Saves game
            if playerInput == "save":
                filename = input("What do you want to name your save file?")
                save_game(board, players, turn, filename)

            #Quit game
            elif playerInput == "quit":
                print("Quitting game")
                break

            cordinates = playerInput.split(" ")
            
            #if coordinates weren't inputted correctly just make the coordinates invalid
            if len(cordinates) < 2:
                cordinates = [0, 0]
            
            #checks that the coordinates are integers
            int(cordinates[0])
            int(cordinates[1])
        except ValueError as e:
            print(f"Error")
            print("Cordinate have to be a number")
            cordinates = [0, 0]

        if board.place_marker(currentPlayer, int(cordinates[0])-1, int(cordinates[1])-1):
            board.search_markers(currentPlayer, int(cordinates[0])-1, int(cordinates[1])-1)
            if currentPlayer.win == True:
                break 
            turn = not turn
            turnC += 1

        #if the board is filled make the game a tie
        if turnC >= board.width * board.height:
            print("It's a tie")
            board.printBoard()
            writeResult(False, players)
            break

    print(f"Game is over")

#adds players and append them into players list
def add_players(name, marker):
    newPlayer = Player(name, marker)
    players.append(newPlayer)
    return newPlayer

def main():
    print(f'''
---Welcome To Noughts and Crosses---
1. or yes to start a new game with either a friend or a bot
2. or load to load and continue playing on a saved game
3. or leaderboard to load statistics and leaderboard
type anything else to quit
    ''')
    command = input("Do you want to play? Input: ").lower()

    #Starts up a new game and builds a new board
    if command == "1" or command == "y" or command == "yes":
        command = input("Type 1 for singelplayer or type 2 for 2 player match Input: ")
        

        if command != "1" and command != "2":
            print("Going back")
            return True

        name = input("Player one what is your name? Name: ")
        add_players(name, "X")

        #if command equals to 2, add a second player
        if command == "2":
            name = input("Player two what is your name? Name: ")
            add_players(name, "O")

        #if singleplayer create a bot
        elif command == "1":
            print("Added bot, get ready.")
            bot = add_players("Bot", "O")
            bot.typeP = "robot"
    
        try:
            size = int(input("How big is the board? Input a number that will equal both height and width of the board. Input: "))
        except ValueError:
            print("width and height have to be an integer, default size will be set")
            size = 3
        
        #if the board size is lower than 5 make the rule 3 in a row to win otherwise 5 in a row to win
        if size < 5:
            rule = 3
        else:
            rule = 5
        
        board = Board(rule, size, size)
        board.create_board()
        turn = False

        play_game(board, turn)
        return True

    #loads a saved game from a json file 
    elif command == "load" or command == "2":
        try:
            filename = input("Which save file do you want to load?")
            loadedData = []
            loadedData = load_game(filename)

        except:
            print("Going back either because you quitted or file not found")
            return True        

        
        
        #assigning old players and old boards from the file to the game
        player = add_players(loadedData['player1']['name'], loadedData['player1']['marker'])
        player.moves = loadedData['player1']['moves']
        player.typeP = loadedData['player1']['typeP']
            
        player = add_players(loadedData['player2']['name'], loadedData['player2']['marker'])
        player.moves = loadedData['player2']['moves']
        player.typeP = loadedData['player2']['typeP']

        board = Board(loadedData['game']['rule'], loadedData['game']['width'], loadedData['game']['height'])
        board.board_grid = loadedData['game']['board_grid']
            
        #once everything is set load up the game
        play_game(board, loadedData['currentTurn'])
        

        return True


    elif command == "3" or command == "leaderboard":
        if not os.path.exists("./slutuppgift/leaderboard.txt") or not os.path.exists("./slutuppgift/results.txt"):
            print("Currently unavailable, try playing a game first!")
        else:
            load_statistics()
        return True
    else:
        return False

while main():
    #clear players list everytime the game ends
    players = []


