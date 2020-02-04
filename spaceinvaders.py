import pygame
import random
import math
from pygame import mixer
import os

 #for playing with sounds in pygame
#initialize pygame
pygame.init()

#print(f'mixer init: {pygame.mixer.init()}')
pygame.mixer.init()
#clock = pygame.time.Clock()
#create a screen                   W   H
screen = pygame.display.set_mode((800,600))

#adding background to our game
background = pygame.image.load('/home/hoddie/Desktop/Questions/Practice/PythonGame/background1.png')

#we load the background sound here
mixer.music.load('background.wav')
mixer.music.play(-1)

#change the title and icon of our window
pygame.display.set_caption('Space invaders')
#adding icon
icon = pygame.image.load('/home/hoddie/Desktop/Questions/Practice/PythonGame/ufo.png')
pygame.display.set_icon(icon)

#adding the player image
playerimg = pygame.image.load('/home/hoddie/Desktop/Questions/Practice/PythonGame/space-invaders.png')
playerX = 370 #the reason for the values in the varibale playerX and Player Y
playerY = 480 # is we want the player to show up somewehre on the screen in our case we want the center
#change in x
playerX_change = 0

#Enemy
enemyimg = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []
numofenemies = 6

for i in range(numofenemies):
    enemyimg.append(pygame.image.load('/home/hoddie/Desktop/Questions/Practice/PythonGame/monster.png'))
    enemy_X.append(random.randint(0, 735 ))#the random lets us spawn enemies any where on the screen
    enemy_Y.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(45)


#BUllets
#ready state you cannot see the bullet on the screen
#fire the bullet is currently moving
bulletimg = pygame.image.load('/home/hoddie/Desktop/Questions/Practice/PythonGame/bullet.png')
bullet_X = 0
bullet_Y = 480
bulletX_change = 0
bulletY_change = 20
bullet_state = 'ready'

#score
score_value = 0
font = pygame.font.Font('/home/hoddie/Desktop/Questions/Practice/PythonGame/dark_tales/Dark Tales.otf', 32) #here were using the inbuilt free font and givingit a size
textX = 10 #these are the x and y values of where you wna tyour text to appear on the screen
textY = 10

#in the function we fist have to render the score before we blit the score on to the screen
def showscore(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i],(x, y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))

def isCollision(enemy_X,enemy_Y,bullet_X,bullet_Y):
    distance = math.sqrt((math.pow(enemy_X - bullet_X,2)) + (math.pow(enemy_Y - bullet_Y, 2)))
    if distance < 27:
        return True
    else:
        return False     

def player(x,y):
    screen.blit(playerimg,(x, y))#we are drawing the player image on the screen using the "blit"

#game loop makes sure the game is always running unless the quit is clicked
running = True
while running:
         #       R G B
    screen.fill((0,0,0))#we set the color of our screen anything u want to continiously show up or run in the game we put it in the while loop        
    screen.blit(background,(0, 0))
    for event in pygame.event.get(): #this is a pygame event that gets all the events in pygame
        if event.type ==  pygame.QUIT: #were checking if the quit is clicked this is a pygame event 
            running = False #if the quit is clicked then we turn the loop to false and we quit the program
        
        #if keystroke is pressed check weather is right or left
        if event.type == pygame.KEYDOWN:
            print('a keystrokes is pressed')
            if event.key == pygame.K_LEFT:
                print('Left arrow is pressed')
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                print('right arrow is pressed')
                playerX_change = 10

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    #gets the cuurent x cordinate of the spaceship or player1
                    bullet_X = playerX
                    fire_bullet(bullet_X, bullet_Y)   
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print('keystroke has be released')
                playerX_change = 0            
            
    
    #here we make sure our spaceship stays with the frame of the assigned window size
    #we take in to cosideration the size of our spacship 
    playerX += playerX_change
    if playerX <=0:
        playerX = 0
    elif playerX >=736:
        playerX = 736    
    
    #same check for boundry for enemy
    for i in range(numofenemies):
        enemy_X[i] += enemyX_change[i]
        if enemy_X[i] <=0:
            enemyX_change[i] = 5
            enemy_Y[i] += enemyY_change[i]
        elif enemy_X[i] >=736:
            enemyX_change[i] = -5  
            enemy_Y[i] += enemyY_change[i]
        
        #collision    
        collision = isCollision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:
            bullet_Y = 480
            bullet_state = "ready" 
            
            score_value += 1
            print(score_value)
            enemy_X[i] = random.randint(0, 735)
            enemy_Y[i] = random.randint(50, 150)
        enemy(enemy_X[i], enemy_Y[i], i)       

    #bullet movement and fire
    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_X,bullet_Y)
        bullet_Y -= bulletY_change
    
    

    #next we call the player and enemy method cause we want the player to always be in the game
    player(playerX,playerY)
    showscore(textX, textY)
    

    #anychange we make u need to create an update this lets pygame update the whole program with newly added features without it no feature will be displayed
    pygame.display.update()
