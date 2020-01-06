import pygame
import random
import os


class Food:
    def __init__(self, width, height):
        """
:param width: Surface width
:param hegiht: Surface height
        """
        self.width = width
        self.height = height
        self.x = round(random.randint(0, width-10) / 10) * 10
        self.y = round(random.randint(0, height-10) / 10) * 10

    def addNew(self):
        self.x = round(random.randint(0, self.width-10) / 10) * 10
        self.y = round(random.randint(0, self.height-10) / 10) * 10

    def draw(self, surf):
        pygame.draw.rect(surf, (0, 0, 0),
                         (self.x-1, self.y-1, 10+2, 10+2))
        pygame.draw.rect(surf, (150, 0, 0),
                         (self.x, self.y, 10, 10))


class Player:
    def __init__(self, x, y, color):
        self.color = color
        self.vel = 10
        self.x = x
        self.y = y
        self.snakeList = []
        self.width = 10
        self.height = 10
        self.xChange = 0
        self.yChange = 0
        self.length = 1
        self.shouldEat = False
        self.shouldDie = False
        self.isOnline = False
        self.isAdmin = False

    def draw(self, surf):
        for p in self.snakeList:
            pygame.draw.rect(surf, (0, 0, 0),
                             (p[0]-1, p[1]-1, self.width+2, self.height+2))
            pygame.draw.rect(surf, self.color,
                             (p[0], p[1], self.width, self.height))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.xChange != -self.vel:
                self.xChange = self.vel
                self.yChange = 0
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.xChange != self.vel:
                self.xChange = -self.vel
                self.yChange = 0
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.yChange != self.vel:
                self.xChange = 0
                self.yChange = -self.vel
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.yChange != -self.vel:
                self.xChange = 0
                self.yChange = self.vel

        # if self.isVerified:
        if self.isAdmin:
            if keys[pygame.K_END]:
                self.eat()

        self.x += self.xChange
        self.y += self.yChange

        if self.x < 0:
            self.x = 990
        if self.x > 990:
            self.x = 0
        if self.y < 0:
            self.y = 690
        if self.y > 690:
            self.y = 0

        if [self.x, self.y] in self.snakeList:
            self.death()

        head = []
        head.append(self.x)
        head.append(self.y)
        self.snakeList.append(head)

        if len(self.snakeList) > self.length:
            del self.snakeList[0]

    def startswith(self, st):
        return False

    def eat(self):
        pygame.mixer.music.load(os.path.join(
            os.path.dirname(__file__), "media/eat.mp3"))
        pygame.mixer.music.play(0, .4)
        self.length += 1

    def death(self):
        if self.length > 1:
            self.xChange = 0
            self.yChange = 0
            self.x = round(random.randint(0, 990) / 10) * 10
            self.y = round(random.randint(0, 690) / 10) * 10
            head = []
            head.append(self.x)
            head.append(self.y)
            self.snakeList = []
            self.snakeList.append(head)
            self.length = 1
