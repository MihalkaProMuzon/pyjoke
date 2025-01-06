import asyncio
import pygame
import os
import math


from gamedata.PlayerControlls import PlayerControlls

class Game:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1,30)
    
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Терминал .Pohg")
        self.clock = pygame.time.Clock()
        
        self.player_controlls = PlayerControlls(self)
        
        self.systems = {}
        self.entities = {}
        self.componments_mapping = {}
                        
    def store_pygame_events(self):
        self.pygame_events = pygame.event.get().copy()
    
    async def start_game(self):
        self.running = True
        await self.main_loop()
    
    async def main_loop(self):
        while self.running:
            self.store_pygame_events()
            #print(type(self.pygame_events))
                 
        
            for event in self.pygame_events:
                if event.type == pygame.QUIT:
                    running = False         

            self.screen.fill((0, 0, 0))
            anim = math.cos(pygame.time.get_ticks() *0.005)
            center = ((320-50) + 100*anim, 240)
            
            pygame.draw.circle(self.screen, (255, 0, 0), center, 50)
            pygame.display.flip()

            self.clock.tick(60) # Ограничение FPS
            await asyncio.sleep(0)  
    