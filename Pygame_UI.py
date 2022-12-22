import pygame, sys, numpy
from Auxiliary_Functions import *

pygame.init()

clock = pygame.time.Clock()
displayx = 800
displayy = 600
display = pygame.display.set_mode((displayx, displayy))

font = pygame.font.SysFont('Comic Sans MS', 15)

def start_screen():

    #defines any necessary variables
    start_button = pygame.Rect(displayx/2 -100, displayy/2 -25, 200, 50)
    exit_button = pygame.Rect(displayx/2 - 100, displayy/2 +50, 200, 50)
    
    start = True
    while start == True:
        exitgamecheck()

        #Renders start menu elements
        display.fill('black')
        
        pygame.draw.rect(display, 'white', start_button, 1)
        pygame.draw.rect(display, 'white', exit_button, 1)

        display.blit(font.render("Start", True, 'white'), start_button)
        display.blit(font.render("Exit", True, 'white'), exit_button)
        
        if checkmousestate(start_button) == True:
            start = False
        elif checkmousestate(exit_button) == True:
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)

def game_screen():

    game_screen = True
    while game_screen == True:

        exitgamecheck()
        playerinput()
        #renders game elements

        player.rect.x = 100
        player.rect.y = 100

        all_sprites_list.update()
        display.fill('black')

    

        all_sprites_list.draw(display) #draws all sprites in their current position
        pygame.display.flip()
        clock.tick(60)


        pass

def gameover_screen():
    pass

def leaderboard_screen():
    pass
