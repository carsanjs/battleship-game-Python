import socket
from _thread import start_new_thread
from game import Game
from board import Board
import pickle

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print("Server started, waiting for connections")
except socket.error as e:
    print(e)


def threaded_client(c, player, gameID):
    global currentPlayers
    c.send(str.encode(str(player)))
    while True:
        # Recibiendo los datos del cliente
        try:
            data_bytes = b""
            new_data = True
            while True:
                if new_data:
                    data_len = int(c.recv(20))
                    new_data = False
                else:
                    packet = c.recv(1024)
                    data_bytes += packet
                    if len(data_bytes) == data_len:
                        break
            data = pickle.loads(data_bytes)

            if gameID in games:
                game = games[gameID]

                if not data:
                    break
                else:
                    # Posicionando el tabero inicialmente
                    if isinstance(data, Board):
                        if player == 0:
                            game.boards[0] = data
                        else:
                            game.boards[1] = data
                    # Gameplay
                    if isinstance(data, tuple):
                        if data[0] == "missed":
                            if player == 0:
                                game.boards[1] = data[1]
                                game.turn = "1"
                            else:
                                game.turn = "0"
                                game.boards[0] = data[1]
                        elif data[0] == "hitted":
                            if player == 0:
                                game.boards[1] = data[1]
                                game.turn = "0"
                            else:
                                game.turn = "1"
                                game.boards[0] = data[1]
                    # Enviando los datos al servidor
                    reply = game
                    if reply:
                        sending_bytes = pickle.dumps(reply)
                        header_sending = "{0:<20}".format(len(sending_bytes))
                        sending = bytes(header_sending, "utf-8") + sending_bytes
                        c.sendall(sending)
            else:
                break
        except:
            break
    print("Lost connection")
    # Manejando los cierres y desconexiones
    try:
        if currentPlayers % 2 == 1:
            del games[gameID]
            print("Closing game {}".format(gameID))
        else:
            game.both_connected = False
    except:
        pass
    currentPlayers -= 1
    c.close()


s.listen()
currentPlayers = 0
games = {}
gameID = 0

while True:
    conn, addr = s.accept()
    print("Connected to {}".format(addr))
    p = 0
    currentPlayers += 1
    game_list = sorted(game for game in games)
    if currentPlayers % 2 == 1:
        if not game_list:
            gameID = 0
            games[gameID] = Game(gameID)
        else:
            for id in range(game_list[-1]+2):
                if id not in game_list:
                    gameID = id
                    games[gameID] = Game(gameID)
                    break
        print("Creating new game: {}".format(gameID))
    else:
        for id in range(game_list[-1]+2):
            if id in game_list and not games[id].both_connected:
                gameID = id
                games[gameID].both_connected = True
                print("Game nr {} has just started".format(gameID))
        p = 1
    start_new_thread(threaded_client, (conn, p, gameID))
