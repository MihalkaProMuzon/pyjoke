import asyncio
import pygame
import os
import math

from abc import ABC, abstractmethod

from gamedata.PlayerControlls import PlayerControlls
from gamedata.Systems.Systems import SystemsManager, SimplePrintSystem

class Game:
    def __init__(self):
        #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0) # Для окна без рамки
        #os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1,30) # Для окна с рамкой
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (-1000,0) # Для убрать нахер с экрана мешает...
        
    
        self._udpclient = None
    
        pygame.init()
        self._screen = pygame.display.set_mode((640, 480), pygame.NOFRAME)
        pygame.display.set_caption("Терминал .Pohg")
        self._clock = pygame.time.Clock()
        
        self._player_controlls = PlayerControlls(self)
        
        self._systems_manager = SystemsManager()
        self._entities = {}
        self._componments_mapping = {}
                        
    def _store_pygame_events(self):
        self.__pygame_events = pygame.event.get().copy()
    
    async def start_game(self, udpclient):
        self._udpclient = udpclient
        self.__running = True
        await self._main_loop()
    
    async def _main_loop(self):   
        
        while self.__running:
            self._store_pygame_events()
            
            await SystemsManager.instance.execute_systems()
            
            
        
            for event in self.__pygame_events:
                if event.type == pygame.QUIT:
                    self.running = False         

            self._clock.tick(60) # Ограничение FPS
            await asyncio.sleep(0)
    