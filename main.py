import math

import pygame
import random
from pygame import mixer

# Initializing Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Title and Icon of our Game
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Background Image
background = pygame.image.load('spacebg.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Aliens
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
numOfAliens= 7
for i in range(numOfAliens):
    alienImg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 150))
    alienX_change.append( 0.3)
    alienY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.8
bullet_state = "ready"

# Player score
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
scoreX = 10
scoreY = 10

# Game Over Text:
gameOverText = pygame.font.Font('freesansbold.ttf',64)

# Game over function:
def gameOver():
    overFont = gameOverText.render("GAME OVER !!!", True, (255, 255, 255))
    screen.blit(overFont, (200, 250))

# This function shows the score
def showScore(x,y):
    show = font.render("Score: "+str(score), True, (255,255,255))
    screen.blit(show, (x,y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))

def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX-bulletX,2)+ math.pow(alienY-bulletY,2))
    if distance <27:
        return True
    else:
        return False

running = True
while running:
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -0.3

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movement of Aliens
    for i in range(numOfAliens):

        # Game Over:
        if alienY[i] >440:
            for k in range(numOfAliens):
                alienY[k] = 2000
            gameOver()
            break
        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 0.3
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.3
            alienY[i] += alienY_change[i]
        # Collision:
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    # Bullet Movement:
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(scoreX,scoreY)
    pygame.display.update()
