import pygame
import random
import math
from pygame import mixer

#Initialize pygame
pygame.init()


#Create the screen. 2 variables, (Hieght, Width).  MUST be inside double parentheses 
screen = pygame.display.set_mode((800,600))


#Title, Icon, Background 32x32 PNG size
pygame.display.set_caption("Space Invaders")
TitleIcon = pygame.image.load('spaceship.png')
pygame.display.set_icon(TitleIcon)
background = pygame.image.load('background.png')

#Sounds
defaultVolume = 0.1
pygame.mixer.music.set_volume(defaultVolume)
mixer.music.load('background.wav')
mixer.music.play(-1) #-1 for loop
bullet_Sound = mixer.Sound('laser.wav')
bullet_Sound.set_volume(0.1)
explosion_Sound = mixer.Sound('explosion.wav')
explosion_Sound.set_volume(0.1)

#X-axis boarder constants
LEFT_WALL = 0
RIGHT_WALL = 736

#Laser
laserIcon = pygame.image.load('laser.png')
laserX = 0 #starting X location
laserY = 480 #starting Y location
#playerX_change = 0 #Not used as it will only be traveling in the Y direction
laserY_change = 3.5 #Speed. Starting Change Value
laser_state = "ready" #Ready = invisible.  Fire = moving

#Player Image 64x64 PNG size
playerIcon = pygame.image.load('xwing.png')
playerX = 370 #starting X location
playerY = 480 #starting Y location
playerX_change = 0 #Speed. Starting Change Value
playerY_change = 0 #Speed. Starting Change Value


#Enemy Image 64x64 PNG size
#Adding multiple enemies.  Erase [] and 'range' iteration if only 1 enemy desired
enemyIcon = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyIcon.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,RIGHT_WALL -1)) #starting X location
    enemyY.append(random.randint(50,150)) #starting Y location
    enemyX_change.append(3) #Speed. Starting Change Value
    enemyY_change.append(30) #Speed. Starting Change Value


#Socre
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) #Font style and size
textX = 10 #Text Location
textY = 10 #Text Location

#Score definition
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,205,145)) #Render first.  Convert INT to STR, set as TRUE, Color of text
    screen.blit(score,(x,y))


#Player definition
def player(x,y): #Draw playerIcon onto the screen.  Blit means to draw
    screen.blit(playerIcon, (x,y)) #When updated, become the new playerX, playerY

#Enemy definition
def enemy(x,y, i): #Draw enemyIcon onto the screen.  Blit means to draw.  Added the 'i' value after creating a list
    screen.blit(enemyIcon[i], (x,y)) #When updated, become the new enemyX, enemyY

#Laser definition
def fire_laser(x,y):
    global laser_state #Global lets you access variable INSIDE of definition
    laser_state = "fire"
    screen.blit(laserIcon, (x+16,y+10)) #+16 to appear center of spaceship. +10 to appear above spaceship

#Collision...and math
#Distance between two points and the midpoint
#Distance = SqrRoot of (x2-x1)^2+(y2-y1)^2
def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX-laserX,2)) + (math.pow(enemyY-laserY,2))) #sqrt = squareroot, pow = ^power
    if distance < 27: #If less than 27 pixels
        #print(distance) #For testing what the distance actually is
        return True
    else:
        False

#Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 32) #Font style and size
def game_over_text():
    over_text = font.render("Game Over.  You destroyed " + str(score_value) + " Invaders.", True, (255,205,145)) #Render first.  Convert INT to STR, set as TRUE, Color of text
    screen.blit(over_text,(100,250))

#Game loop
running = True
while running:
    #RGB for screen
    screen.fill((0,0,0)) #Draw screen 1st
    #Background image
    screen.blit(background,(0,0))
    for event in pygame.event.get(): #Get any event
        if event.type == pygame.QUIT: #Check if a specific event happened
            running = False #Change variable 'running' if pygame.QUIT happened
    
    #If keystroke is pressed, check if it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3 #If the LEFT key is down, move left
            if event.key == pygame.K_RIGHT:
                playerX_change = +3 #If the RIGHT key is down, move right
            if event.key == pygame.K_SPACE:
                if laser_state == "ready": #Prevents current laser update for multiple spacebar presses 
                    bullet_Sound.play()
                    laserX = playerX #If Spacebar is pressed, current laserX take the position value of playerX
                    fire_laser(laserX,laserY)  

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0 #If either key is released, stop moving

    playerX += playerX_change #Update playerX variable value by the amount of the key pressed 

    #Contain player image within screen window
    if playerX <= LEFT_WALL: #If the image goes left and reaches 0
        playerX = LEFT_WALL #Continuously assign possition as the defined constant variable 
    elif playerX >= RIGHT_WALL: #If the image goes right and reaches 736 (screen size minus image size)
        playerX = RIGHT_WALL #Continuously assign possition as the defined constant variable

    enemyX += enemyX_change #Update enemyX variable value by the amount of the key pressed 

    #Contain enemy image within screen window
    for i in range(num_of_enemies): #Added when adding .append().  Take out for only 1 enemy


        #Game Over
        if enemyY[i] > 440: #If one of the enemies in the list is greater than 440 pixels
            for j in range(num_of_enemies): #Enemies put in new list called 'j'
                enemyY[j] = 2000 #Move all enemies 
            game_over_text()
            break #Break out of enemy loop

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= LEFT_WALL: #If the image goes left and reaches 0
            enemyX_change[i] = 2 #Continuously assign possition as the defined constant variable
            enemyY[i] += enemyY_change[i] #When enemy hits the boarder, drop down by the enemyY_change value
        elif enemyX[i] >= RIGHT_WALL: #If the image goes right and reaches 736 (screen size minus image size)
            enemyX_change[i] = -2 #Continuously assign possition as the defined constant variable
            enemyY[i] += enemyY_change[i] #When enemy hits the boarder, drop down by the enemyY_change value
    
        #Collision Check. MAKE SURE INSIDE FOR LOOP no that it has been added to the loop
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosion_Sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,RIGHT_WALL -1) #Reset enemy X location
            enemyY[i] = random.randint(50,150) #Reset enemy Y location    

        enemy(enemyX[i],enemyY[i],i) #Draw enemy next. Take the variables enemyX/enemyY and send it to 'def enemy(x,y)'

    #Laser movement
    if laserY <=0:
        laserY = 480
        laser_state = "ready" #Set laser to 'ready' if it passes above y-axis 0
    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change
        


    player(playerX,playerY) #Draw player next. Take the variables playerX/playerY and send it to 'def player(x,y)'
    show_score(textX,textY)
    pygame.display.update() #Update screen