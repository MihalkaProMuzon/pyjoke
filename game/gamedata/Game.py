import pygame

class Game:
    def __init__(self, _pygame: pygame):
        self.pygame = _pygame
        self.player_controlls = None
        self.screen = None
        self.events = None
        
    def init(self, _screen, _player_controlls):
        self.screen = _screen
        self.player_controlls = _player_controlls
        
    def set_screen(self, _screen):
        self.screen = _screen
        
    def store_events(self):
        self.events = self.pygame.event.get()
        