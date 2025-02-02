import pygame
import asyncio

from gamedata.PlayerControlls import PlayerControlls
from gamedata.Game import Game
from gamedata.Racket import Racket


###  CONFIG  ###################################################################################
BG_COL = (30,0.0,0.0)

################################################################################################


async def main():
    pygame.init()
    screen = pygame.display.set_mode((800,500))    
    pygame.display.set_caption("Терминал pohg")
    
    
    game = Game(pygame)
    player_controlls = PlayerControlls(game)
    game.init(screen, player_controlls)
    
    cvadrat = Racket(game)
    
    while True:
        game._store_pygame_events()
        for event in game.__pygame_events:
            if event.type == pygame.QUIT:
                return
        
        game.__player_controlls.handle_controlls()
    
        screen.fill( BG_COL )
        
        # **
        cvadrat.update()
        cvadrat.draw()
        # **
    
        pygame.display.flip()
        #await asyncio.sleep(0.03)
        
    
if __name__ == "__main__":
    asyncio.run(main())