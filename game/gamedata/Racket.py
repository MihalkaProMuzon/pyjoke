import pygame
from gamedata.Game import Game

class Racket:
    def __init__(self, game: Game):
        self.pos_x = 0
        self.pos_y = 0
        self.speed = 0.2
        self.game = game

    def update(self):
        # Update pos
        if self.game.__player_controlls.right:
            self.pos_x += self.speed
        if self.game.__player_controlls.left:
            self.pos_x -= self.speed
        if self.game.__player_controlls.up:
            self.pos_y -= self.speed
        if self.game.__player_controlls.down:
            self.pos_y += self.speed


    def draw(self):
        self.game.pygame.draw.rect(self.game._screen,(255,255,255), (self.pos_x, self.pos_y, 50, 50),100, 3)