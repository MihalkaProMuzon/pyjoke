import pygame


draws = 0


################  PlayerControlls  #############################################################
class PlayerControlls:
    def __init__(self):
        self.left = False
        self.right = False
        self.up = False
        self.down = False

################################################################################################

################  racket #######################################################################
class Racket:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0

    def update(self):
        # Update pos
        if player_controlls.right:
            self.pos_x += 1
        if player_controlls.left:
            self.pos_x -= 1
        if player_controlls.up:
            self.pos_y -= 1
        if player_controlls.down:
            self.pos_y += 1
            

    def draw(self, surface):
        pygame.draw.rect(surface,(255,255,255), (self.pos_x, self.pos_y, 50, 50),100, 3)
        

################################################################################################


player_controlls = PlayerControlls()
BG_COL = (30,0.0,0.0)


def run():
    pygame.init()
    screen = pygame.display.set_mode((800,500))    
    pygame.display.set_caption("Терминал pohg")
    
    cvadrat = Racket()   
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_LEFT:
                        player_controlls.left = True
                    case pygame.K_RIGHT:
                        player_controlls.right = True
                    case pygame.K_DOWN:
                        player_controlls.down = True
                    case pygame.K_UP:
                        player_controlls.up = True
            
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_LEFT:
                        player_controlls.left = False
                    case pygame.K_RIGHT:
                        player_controlls.right = False
                    case pygame.K_DOWN:
                        player_controlls.down = False
                    case pygame.K_UP:
                        player_controlls.up = False
    
        screen.fill( BG_COL )
        
        cvadrat.update()
        cvadrat.draw(screen)
    
        pygame.display.flip()
    
run()