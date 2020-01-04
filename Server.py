import sys
import socket
import pickle
from Player import Player, Food
from random import randint
from _thread import *

ip = "127.0.0.1"
port = 5555

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((ip, port))

serv.listen()
print("Server listening at {}.".format(ip+":"+str(port)))

players = []
foods = []
logList = []
clientCount = 0


def threaded_function(conn, player):
    conn.send(pickle.dumps(players[player]))

    while True:
        for f in foods:
            if players[player].x == f.x and players[player].y == f.y:
                players[player].shouldEat = True
                foods[foods.index(f)].addNew()

        for p in players:
            if p != players[player]:
                if [players[player].x, players[player].y] in p.snakeList:
                    players[player].death()

        reply = []
        try:
            data = pickle.loads(conn.recv(4096*12))
        except:
            data = None

        if not data:
            print("Disconnected")
            players[player].isOnline = False
            del foods[0]
            break
        elif type(data) == Player:
            players[player] = data
            players[player].isOnline = True
            for p in players:
                if players.index(p) != player:
                    reply.append(p)

            # print("get --> " + str(data))
            # print("post --> " + str(reply))
            try:
                conn.sendall(pickle.dumps(reply))
            except:
                conn.sendall(pickle.dumps([]))
        elif data == "getPlayer":
            conn.sendall(pickle.dumps(players[player]))
        elif data.startswith("^AdminAccess$="):
            d = data[14:]
            if d == "qwe123qwe123":
                players[player].isAdmin = True
                conn.sendall(pickle.dumps(players[player]))
            else:
                conn.sendall(pickle.dumps("Wrong password!"))
        else:
            conn.sendall(pickle.dumps(foods))

    conn.close()
    # del players[player]
    # clientCount -= 1
    return


while True:
    conn, addr = serv.accept()
    print("Connected from %s." % str(addr))
    logList.append("New Player Connected.")
    players.append(
        Player(round(randint(0, 990) / 10) * 10, round(randint(0, 690) / 10) * 10, (randint(0, 100), randint(0, 100), randint(0, 100))))
    foods.append(Food(1000, 700))

    start_new_thread(threaded_function, (conn, clientCount))
    clientCount += 1
