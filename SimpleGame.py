import pygame
import sys
from Network import Network
import time
from socket import *
import os
from _thread import *
import tkinter as tk
import keyboard

pygame.init()

w, h = (1000, 700)
win = pygame.display.set_mode((w, h))
pygame.display.set_caption("Client")

Roboto = {
    "Thin": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-Thin.ttf"), 35),
    "Black": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-Black.ttf"), 35),
    "italic": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-italic.ttf"), 35),
    "BlackItalic": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-BlackItalic.ttf"), 35),
    "Light": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-Light.ttf"), 35),
    "LightItalic": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-LightItalic.ttf"), 35),
    "ThinItalic": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-ThinItalic.ttf"), 35),
    "Medium": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-Medium.ttf"), 35),
    "MediumItalic": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-MediumItalic.ttf"), 35),
    "Regular": pygame.font.Font(os.path.join(os.path.dirname(__file__), "Roboto/Roboto-Regular.ttf"), 35),
}


def redrawWindow(surf, player, players, foods):
    scores = []
    for p in sorted(players, key=lambda x: x.length, reverse=True):
        if p.isOnline:
            p.draw(surf)
            scores.append(Roboto["Regular"].render(
                "Score: %s" % str(len(p.snakeList)), 1, p.color))

    for f in foods:
        f.draw(surf)

    player.draw(surf)

    playerScore = Roboto["Regular"].render(
        "Score: %s" % str(len(player.snakeList)), 1, player.color)

    win.blit(playerScore, (10, 10))
    x = playerScore.get_height() + 20
    for s in scores:
        win.blit(s, (10, x))
        x += s.get_height() + 10
    pygame.display.update()


def run():    
    changePlayer = False
    clock = pygame.time.Clock()
    n = Network("127.0.0.1", 5555)    
    def admin():    
    
        root = tk.Tk()
    
        var = tk.StringVar()
    
        ent = tk.Entry(root, textvariable=var)    
        ent.pack()
    
        def check(v):
            x = n.send("^AdminAccess$="+v.get()) 
            n.player = x if type(x) != str else n.player
            changePlayer = True
            root.destroy()
        but = tk.Button(root, text="Login", command=lambda: check(var))    
        but.pack()
    
        root.mainloop()
    
    keyboard.add_hotkey("F2", admin)
    while True:
        player = n.player
        gameOver = False
        while not gameOver:
            if changePlayer:
               player.isAdmin = True
               changePlayer = False
            clock.tick(30)
            win.fill((170, 170, 170))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    sys.exit()

            player.move()

            players = n.send(player)
            uPlayer = n.send("getPlayer")
            if uPlayer.shouldEat:
                player.eat()
            foods = n.send("foods")

            redrawWindow(win, player, players, foods)


run()
