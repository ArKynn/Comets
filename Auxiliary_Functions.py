import math, pygame, sys, Pygame_UI, numpy
from pygame.locals import *

def checkmousestate(button):
    if button.collidepoint(pygame.mouse.get_pos()):  #Based on answer by skrx on StackOverfow (https://stackoverflow.com/questions/44998943/how-to-check-if-the-mouse-is-clicked-in-a-certain-area-pygame)
        pygame.draw.rect(Pygame_UI.display, 'red', button, 1)
        for event in pygame.event.get(eventtype=MOUSEBUTTONDOWN):
            if event.button == 1:
                return True

def exitgamecheck(): #If window X is pressed, shutsdown program
    for event in pygame.event.get(eventtype = pygame.QUIT):
        pygame.quit()
        sys.exit()

p0 = [9, 0]
p1 = [0, 24]
p2 = [9, 18]
p3 = [18, 24]



class sprite(pygame.sprite.Sprite): 
    def __init__(self, width, height, poligon, pos_x, pos_y):
        super().__init__()
        
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.poligon = poligon #Poligon Which will be rendered in the player position
        pygame.draw.lines(self.image, 'white', True, poligon, 2) #renders a poligon inside the sprite surface
        
player = sprite(18, 24, [p0, p1, p2, p3], 100, 100)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)


def playerinput(): #recieves player input and returns an effect
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        pass
    if key[pygame.K_SPACE]:
        pass
    if key[pygame.K_LEFT]:
        player_rotation(1, player)
    if key[pygame.K_RIGHT]:
        player_rotation(-1, player)


def player_rotation(ang, object):
    pass