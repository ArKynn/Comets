import pygame, sys

from pygame.math import Vector2

from pygame.locals import *

import math

import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)

pygame.init()

# Definition of screen limits
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# screen initialization
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fpsClock=pygame.time.Clock()
FPS = 30 

# Some code below was adapted from a basic tutorial game in pygame: https://realpython.com/pygame-a-primer/ 

# Define the Player object by extending pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, position:Vector2):
        super(Player, self).__init__()
        self.surf = pygame.image.load("player.png").convert()
        self.surf = pygame.transform.scale(self.surf , (self.surf.get_rect().width*0.2, self.surf.get_rect().height*0.2))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.position = position
        self.velocity = Vector2(0,0)
        self.rect.center = position
        self.shoot_timer = None
        self.angle = 0

    def update(self, pressed_keys):
        self.position = wrap_around(self.position, 10)  
        self.position = self.position + self.velocity
        self.rect.center = self.position

        # for rotation tests - not used anymore
        #self.surf.fill((0,0,0))
        #posToAdd = Vector2(0,20)
        #posToAdd = posToAdd.rotate(self.angle)
        #pygame.draw.line(self.surf, (60, 179, 113), Vector2(20,20), posToAdd+Vector2(20,20), 5)

        # timer to avoid shooting continuosly
        if self.shoot_timer is not None:
            if pygame.time.get_ticks()-self.shoot_timer > 500:
                self.shoot_timer = None

        if pressed_keys[K_SPACE] and self.shoot_timer == None:
            self.shoot_timer = pygame.time.get_ticks()
            new_bullet = Bullet(self.position, self.velocity + Vector2(0,-5).rotate(self.angle))
            bullets.add(new_bullet)

        if pressed_keys[K_UP]:
            velToAdd = Vector2(0,0.1)
            velToAdd = velToAdd.rotate(self.angle)
            self.velocity = self.velocity - velToAdd

        if pressed_keys[K_DOWN]:
            velToAdd = Vector2(0,0.1)
            velToAdd = velToAdd.rotate(self.angle)
            self.velocity = self.velocity + velToAdd

        if pressed_keys[K_LEFT]:
            self.angle = self.angle - 5
            if self.angle>360:
                self.angle=0
            if self.angle<0:
                self.angle=360     
            self.rotateSprite()

        if pressed_keys[K_RIGHT]:
            self.angle = self.angle + 5
            if self.angle>360:
                self.angle=0
            if self.angle<0:
                self.angle=360
            self.rotateSprite()

        # speed limiter
        if self.velocity.x>10:
            self.velocity.x=10
        if self.velocity.x<-10:
            self.velocity.x=-10
        if self.velocity.y>10:
            self.velocity.y=10
        if self.velocity.y<-10:
            self.velocity.y=-10
           
    # Function to rotate an image based on example in https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    def rotateSprite(self):
        image_rect = self.rect

        offset_center_to_pivot = self.position - image_rect.center
    
        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(self.angle)

        # rotated image center
        rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)

        # get a rotated image
        self.surf = pygame.image.load("player.png").convert()
        self.surf = pygame.transform.scale(self.surf , (self.surf.get_rect().width*0.2, self.surf.get_rect().height*0.2))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.rotate(self.surf, -self.angle)
        self.rect  = self.surf.get_rect(center = rotated_image_center)


# Define the Comet object by extending pygame.sprite.Sprite
class Comet(pygame.sprite.Sprite):
    def __init__(self, position:Vector2, velocity:Vector2, level, level1_ID):
        super(Comet, self).__init__()
        self.surf = pygame.image.load("comet.png").convert()
        self.surf = pygame.transform.scale(self.surf , (self.surf.get_rect().width/(2*level), self.surf.get_rect().height/(2*level)))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.position = position
        self.velocity = velocity
        self.lvl = level #Big = 1, Med = 2, Small = 3
        self.angle = random.randint(0,360)
        self.angle_rot = random.random()*level-level/2  
        self.level1_ID = level1_ID
    
    # Move and Rotate Comet based on constant speeds
    def update(self):
        self.position = wrap_around(self.position, 40/self.lvl)  
        self.position = self.position + self.velocity
        self.rect.center = self.position
        self.angle = self.angle + self.angle_rot
        self.rotateSprite()

    # Function to rotate an image based on example in https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
    def rotateSprite(self):
        image_rect = self.rect

        offset_center_to_pivot = self.position - image_rect.center
    
        # rotated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(self.angle)

        # rotated image center
        rotated_image_center = (self.position.x - rotated_offset.x, self.position.y - rotated_offset.y)

        # get a rotated image
        self.surf = pygame.image.load("comet.png").convert()
        self.surf = pygame.transform.scale(self.surf , (self.surf.get_rect().width/(2*self.lvl), self.surf.get_rect().height/(2*self.lvl)))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = pygame.transform.rotate(self.surf, -self.angle)
        self.rect  = self.surf.get_rect(center = rotated_image_center)


# Define the Bullet object by extending pygame.sprite.Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position:Vector2, velocity:Vector2):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load("bullet.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect() 
        self.position = position
        self.velocity = velocity
        self.timeLimit = 4 #seconds
        self.rect.center = position
        self.self_timer = pygame.time.get_ticks()
    
    # Move Bullet 
    def update(self):  
        self.position = self.position + self.velocity
        self.rect.center = self.position
       
        # Expires bullet after time limit
        if pygame.time.get_ticks()-self.self_timer > self.timeLimit*30*FPS:
            self.kill()

# Section with helper functions

# Comet spawner   
def comets_spawn(comet: Comet):
    if comet.lvl < 3:
        new_lvl = comet.lvl+1
        rl = new_lvl*2
        nr_of_comets_to_spawn = 3 if comet.lvl == 1 else 5
        for i in range(1, nr_of_comets_to_spawn + 1):
            new_comet = Comet(comet.position + Vector2(random.randint(0,100)-50,random.randint(0,100)-50),Vector2(random.random()*rl-rl/2,random.random()*rl-rl/2),new_lvl, comet.level1_ID)
            comets.add(new_comet)

# collision between player and any comet
def player_collision(player: Player, comets):
    collider:Player = pygame.sprite.spritecollideany(player, comets)
    if collider:
        player.kill()
        collider.kill()       
    return collider != None
    
# collision between a bullet and any comet
def bullet_collision(bullet: Bullet, comets):
    collider:Comet = pygame.sprite.spritecollideany(bullet, comets)
    if collider:
        bullet.kill()
        comets_spawn(collider)
        if collider.lvl==3:
            comet_level1_trailer[collider.level1_ID] = comet_level1_trailer[collider.level1_ID] - 1
            if comet_level1_trailer[collider.level1_ID] <= 0:
                spawn_new_level1_comet(Vector2(random.randint(0,100),random.randint(0,100)),Vector2(random.random()*4-2,random.random()*4-2))
        collider.kill()

# level 1 comet spawner
def spawn_new_level1_comet(position, velocity):
    new_comet = Comet(position, velocity, 1, len(comet_level1_trailer))
    comets.add(new_comet)
    comet_level1_trailer.append(15)

# function to wrap around the screen the movement/position of the comets and player    
def wrap_around(cur_pos:Vector2, margin):
    if cur_pos.x < -margin:
        cur_pos.x = SCREEN_WIDTH + margin
    if cur_pos.x > SCREEN_WIDTH + margin:
        cur_pos.x = -margin
    if cur_pos.y < -margin:
        cur_pos.y = SCREEN_HEIGHT + margin
    if cur_pos.y > SCREEN_HEIGHT + margin:
        cur_pos.y = -margin
    return cur_pos


#testing section

# create sprite groups to help iterate and colisions
bullets = pygame.sprite.Group()
comets = pygame.sprite.Group()
players = pygame.sprite.Group()

# spawn player in the middle of the screen
new_player = Player(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
players.add(new_player)

#background image
bg = pygame.image.load("bg.png")

comet_level1_trailer = []

#spawn 2 Level 1 comets on random locations, with random speeds
spawn_new_level1_comet(Vector2(random.randint(0,100),random.randint(0,100)),Vector2(random.random()*4-2,random.random()*4-2))
spawn_new_level1_comet(Vector2(random.randint(700,800),random.randint(500,600)),Vector2(random.random()*4-2,random.random()*4-2))

# marker to maintain game status
Game_Ended = False

# main loop for testing purposes
while True: #not Game_Ended:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    new_player.update(pressed_keys)
            
    bullets.update()
    comets.update()

    # collisions
    for entity in bullets:
        bullet_collision(entity, comets)

    for entity in players:
        if player_collision(entity, comets):
                Game_Ended = True

    screen.blit(bg, bg.get_rect())

    for entity in players:
        screen.blit(entity.surf, entity.rect)
    for entity in bullets:
        screen.blit(entity.surf, entity.rect)
    for entity in comets:
        screen.blit(entity.surf, entity.rect)

    pygame.display.update()
    fpsClock.tick(FPS)

#pygame.quit()
#sys.exit()