import pickle
from socket import *
from tkinter import *
from functools import partial


class Network:
    def __init__(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.addr = (ip, port)
        self.player = self.connect()
        self.isWorking = True

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.isWorking = True
            return pickle.loads(self.client.recv(4096*12))
        except error as e:
            print(e)
            self.isWorking = False

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096*12))
        except error as e:
            print(e)
            self.client = socket(AF_INET, SOCK_STREAM)
            self.player = self.connect()
