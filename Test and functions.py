import pygame, sys, time

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

pygame.init()
pygame.font.init()

# Definition of screen limits
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# screen initialization
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#font initialization
gameoverfont = pygame.font.SysFont('Corbel', 50)
gamefont = pygame.font.SysFont('Corbel', 17)

fpsClock=pygame.time.Clock()
FPS = 30 



"Game init"
def Gameinit():
    global players, new_player, bullets, bullet_collision, comets, bg, player_collision
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
        global Score

        collider:Comet = pygame.sprite.spritecollideany(bullet, comets)
        if collider:
            Score += 1 #Increments score for each comet kill
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


"Game Over UI"
#Renders Game_Over over the screen for 3 seconds
def Game_Over():
    global Game_End, start_time

    for event in pygame.event.get(eventtype=pygame.QUIT):
        pygame.quit()
        sys.exit()

    #renders GameOver on screen
    screen.blit(gameoverfont.render("Game Over", True, 'White'), (SCREEN_WIDTH/2 -100, SCREEN_HEIGHT/2 -25))

    #gets current time, if 3 seconds since gameover have passed, proceed to leaderboard
    if (time.time() - start_time) > 3:
        Game_End = False
    
    pygame.display.update()
    fpsClock.tick(FPS)



"Start Screen UI"
def Start_screen():
    global startscreen

    def checkmousestate(button):
        if button.collidepoint(pygame.mouse.get_pos()):  #Based on answer by skrx on StackOverfow (https://stackoverflow.com/questions/44998943/how-to-check-if-the-mouse-is-clicked-in-a-certain-area-pygame)
            pygame.draw.rect(screen, 'red', button, 1)
            for event in pygame.event.get(eventtype=MOUSEBUTTONDOWN):
                if event.button == 1:
                    return True
    
    #defines any necessary variables
    start_button = pygame.Rect(SCREEN_WIDTH/2 -100, SCREEN_HEIGHT/2 -25, 200, 50)
    exit_button = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 +50, 200, 50)
    
    for event in pygame.event.get(eventtype=pygame.QUIT):
        pygame.quit()
        sys.exit()

    #Renders start menu elements
    screen.fill('black')
    
    pygame.draw.rect(screen, 'white', start_button, 1)
    pygame.draw.rect(screen, 'white', exit_button, 1)

    screen.blit(gameoverfont.render("Comets", False, 'white'), (SCREEN_WIDTH/2 - 87, 100))
    screen.blit(gamefont.render("Start", False, 'white'), (start_button[0] +75, start_button[1] +15))
    screen.blit(gamefont.render("Exit", False, 'white'), (exit_button[0] +75, exit_button[1] +15))
    
    if checkmousestate(start_button) == True:
        startscreen = False
    elif checkmousestate(exit_button) == True:
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    fpsClock.tick(FPS)



"Leaderboard UI"
#Renders a leaderboard, asks for initials if score in top 10
def Leader_board_screen():
    global Score, score_already_checked

    for event in pygame.event.get(eventtype=pygame.QUIT):
        pygame.quit()
        sys.exit()
    
    allkeys = { #needed to input initials for score 
    K_a : "A",
    K_b : "B",
    K_c : "C",
    K_d : "D",
    K_e : "E",
    K_f : "F",
    K_g : "G",
    K_h : "H",
    K_i : "I",
    K_j : "J",
    K_k : "K",
    K_l : "L",
    K_m : "M",
    K_n : "N",
    K_o : "O",
    K_p : "P",
    K_q : "Q",
    K_r : "R",
    K_s : "S",
    K_t : "T",
    K_u : "U",
    K_v : "V",
    K_w : "W",
    K_x : "X",
    K_y : "Y",
    K_z : "Z",
}   
    if score_already_checked == False: #Because this is inside a loop, this prevents the following code to loop

        with open('Leaderboard.txt', 'r+') as fread: #opens leaderboard.txt in read and write mode:
            leaderboardtext = fread.readlines()
            line_num = -1 #keeps track of current line number
            for line in leaderboardtext: #checks each line for a score
                line_num += 1
                saved_score = line[4] + line[5] + line[6] + line[7] #temporarily saves the read score
                if Score > 0:
                    if int(saved_score) < Score: #checks is saved score is smaller than current score

                        initials = "" 
                        while len(initials) < 3:
                            
                            screen.fill('black')
                            
                            pygame.draw.rect(screen, 'white', (SCREEN_WIDTH/2 -152, 48, 304, 504))
                            pygame.draw.rect(screen, 'black', (SCREEN_WIDTH/2 -150, 50, 300, 500))
                            screen.blit(gamefont.render("Insert your 3 initials", False, 'white'), (SCREEN_WIDTH/2 - 75, SCREEN_HEIGHT/2 - 25))
                            screen.blit(gamefont.render(f"Initials : {initials}", False, 'white'), (SCREEN_WIDTH/2 - 25, SCREEN_HEIGHT/2))
                            
                            for event in pygame.event.get(eventtype=KEYDOWN):
                                try:
                                    initials = initials + allkeys[event.key] #adds the pressed key to the initials string
                                except KeyError:
                                    pass    
                            pygame.display.update()
                            fpsClock.tick(FPS)
                            
                        strscore = str(Score) #converts score to a string
                        while len(strscore) < 4: #checks if score's number of algarisms is smaller than 4 
                            strscore = "0" + strscore #adds 0s so the score gets into a 4 algarism number
                        strscore = strscore + "\n"

                        new_score = f"{initials} {strscore}" #gets initals and score together in a string
                        leaderboardtext.insert(line_num, new_score) #writes initials and score into the current line

                        Score = 0
                        del leaderboardtext[10] #deletes top 11 from leaderboard list

                        with open('Leaderboard.txt', 'w') as fwrite:
                            for line in leaderboardtext:
                                fwrite.write(line)

                        

                        score_already_checked = True

    start_time = time.time()

    Leader_board_Render = True            
    while Leader_board_Render == True:
        
        for event in pygame.event.get(eventtype=pygame.QUIT):
            pygame.quit()
            sys.exit()

        pygame.draw.rect(screen, 'white', (SCREEN_WIDTH/2 -152, 48, 304, 504))
        pygame.draw.rect(screen, 'black', (SCREEN_WIDTH/2 -150, 50, 300, 500))
        screen.blit(gamefont.render("Top 10", False, 'white'), (SCREEN_WIDTH/2 -25, 75))

        with open('Leaderboard.txt', 'r+') as fread: 
            n = 0  #Increments for every line in leaderboard.txt, rendering every line one above another
            for line in fread:
                n += 1
                screen.blit(gamefont.render(line.replace('\n',""), False, 'white'), (SCREEN_WIDTH/2 -35, 150 + 25 * n))
        
        if (time.time() - start_time) > 6:
            Leader_board_Render = False


        pygame.display.update()
        fpsClock.tick(FPS)



"Game Screen UI"   
def Game_screen():
    global gameloop
    
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
                gameloop = False

    screen.blit(bg, bg.get_rect())

    for entity in players:
        screen.blit(entity.surf, entity.rect)
    for entity in bullets:
        screen.blit(entity.surf, entity.rect)
    for entity in comets:
        screen.blit(entity.surf, entity.rect)

    screen.blit(gamefont.render(f"Score: {Score}", False, 'white'), (SCREEN_WIDTH/2 - 25, 50))
    
    pygame.display.update()
    fpsClock.tick(FPS)


# variable to track score
Score = 0

# variable to check when gameover and leaderboard start
check = 0


"""MAIN LOOP"""

while True:
    startscreen = True
    while startscreen == True:
        Start_screen()

    Gameinit()

    gameloop = True
    while gameloop == True: #not Game_Ended:
        Game_screen()
        

    #gets current time and sets a duration
    max_time = 3
    start_time = time.time()

    Game_End = True
    while Game_End == True:
        Game_Over()
    

    score_already_checked = False
    Leader_board_screen() #This screen is out of a loop as it already has a loop internaly
    


#pygame.quit()
#sys.exit()