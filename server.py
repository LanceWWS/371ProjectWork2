import socket
from _thread import *
import sys
import pickle
from game import Game

server = "10.0.0.8" #add your server address here
port = 5555

MAX_PLAYERS = 4

connected = set()
games = {}
client = {}
idCount = 0

#currently set up TCP, but may change
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    
s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn, p, gameId):
    global idCount
    print(str.encode(str(p)), "encodeing", str(p))
    conn.send(str.encode(str(p)))
    print(f"Sending player ID {p} to {conn.getpeername()}")

    reply = ""
    while True:
        try:
            print("Waiting for data...")
            data = conn.recv(4096).decode()

            #check if the gameId is valid
            if gameId in games:
                print("GameId is valid")
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
            
            #check game data and if over
            if data['type'] == 'paint':
                x, y = data['x'], data['y']
                game.paint(x, y, p)

            send_data = {
                'type': 'state',
                'grid': game.grid,
                'current_player': game.current_player,
                'scores': game.get_scores(),
                'winner': game.get_winner() if game.is_game_over() else None
            }
            conn.sendall(pickle.dumps(send_data))

        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()
    
while True:
    conn , addr = s.accept()
    print("Connected to:", addr)
  
    
    p = idCount % MAX_PLAYERS  # Alternate player IDs, e.g., 0, 1, 2, 3
    idCount += 1
    # Determine which game the player should join
    gameId = idCount // MAX_PLAYERS  # Integer division gives the game ID

    # Create a new game if this is the first player for the game
    if p == 0:
        games[gameId] = Game(num_players=MAX_PLAYERS)  # Adjust based on MAX_PLAYERS
        print(f"Creating new game {gameId}...")
    else:
        print(f"Player {p} joined game {gameId}")
        games[gameId].num_players = MAX_PLAYERS  # Ensure this game has the correct number of players

    start_new_thread(threaded_client, (conn, p, gameId))