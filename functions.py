
import pygame

from pygame.math import Vector2

from pygame.locals import *
import math

import random


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#some code was adapted from a tutorial game in pygame

# Define the Bullet object by extending pygame.sprite.Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.init()

    def init(self):
        self.surf = pygame.image.load("bullet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    
    # Move Bullet 
    def update(self):
         pass


# Define the Comet object by extending pygame.sprite.Sprite
class Comet(pygame.sprite.Sprite):
    def __init__(self, velocity, position:Vector2):
        super(Comet, self).__init__()
        self.surf = pygame.image.load("comet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.velocity = velocity
        self.position = position
        self.lvl = 1 #Big = 1, Med = 2, Small = 3

    # Move Comet based on a constant speed
    def update(self):
        wrap_around(self.position.x,self.position.y)  
        #to do -> self.position
            


# Define the Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("player.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()


def shoot_bullet(player: Player):
    new_bullet = Bullet()
    #to do -> new_bullet.ang = player.ang
    

def comets_spawn(comet: Comet):
    if comet.lvl < 3:
        nr_of_comets_to_spawn = 3 if comet.lvl == 1 else 5
        for i in range(1, nr_of_comets_to_spawn + 1):
            new_comet = Comet()
            new_comet.lvl = comet.lvl + 1
     

#colision between player and any comet
def player_colision(player: Player, comets):
    collider = pygame.sprite.spritecollideany(player, comets)
    if collider:
        player.kill()
    
#colision between a bullet and any comet
def bullet_colision(bullet: Bullet, comets):
    collider = pygame.sprite.spritecollideany(bullet, comets)
    if collider:
        bullet.kill()
        comets_spawn(collider)
        collider.kill()

    









def wrap_around (cur_pos_x, cur_pos_y):
    if cur_pos_x < 0:
        cur_pos_x = SCREEN_WIDTH
    if cur_pos_x > SCREEN_WIDTH:
        cur_pos_x = 0
    if cur_pos_y < 0:
        cur_pos_y = SCREEN_HEIGHT
    if cur_pos_y > SCREEN_HEIGHT:
        cur_pos_y = 0






pygame.draw.line(display,'white', (400, 400), (400+math.cos(ang)*100, 400+math.sin(ang)*100))