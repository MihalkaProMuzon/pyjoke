import pygame

class PlayerControlls:
    def __init__(self, game):
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.game = game
            
    def handle_controlls(self):
        for event in self.game.pygame_events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        self.left = True
                    case pygame.K_RIGHT:
                        self.right = True
                    case pygame.K_DOWN:
                        self.down = True
                    case pygame.K_UP:
                        self.up = True
            
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT:
                        self.left = False
                    case pygame.K_RIGHT:
                        self.right = False
                    case pygame.K_DOWN:
                        self.down = False
                    case pygame.K_UP:
                        self.up = False