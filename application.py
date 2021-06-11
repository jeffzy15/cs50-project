import random
import math
import pygame
from pygame import mixer
from time import sleep
import easygui

easygui.msgbox("Get a score of 30 to WIN. Click OK to begin game. Designed by: jeffzy15", title="Notification")

# Initialise the pygame
pygame.init()
pygame.font.init()

# Create the Window
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("images/background.png")

# Background Music
mixer.music.load("audio/background.wav")
mixer.music.play(-100)

# Title and Icon

pygame.display.set_caption("Return of the Aliens")
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

# Player

Player_Image = pygame.image.load("images/player.png")
PlayerX = 370
PlayerY = 480
Player_X_Change = 0

# Enemy

Enemy_Image = []
EnemyX = []
EnemyY = []
Enemy_X_Change = []
Enemy_Y_Change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    Enemy_Image.append(pygame.image.load("images/enemy.png"))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    Enemy_X_Change.append(4)
    Enemy_Y_Change.append(40)

# Bullet

# Ready - You cannot see the bullet
# Fire - You can see the bullet
Bullet_Image = pygame.image.load("images/bullet.png")
BulletX = 0
BulletY = 480
Bullet_X_Change = 0
Bullet_Y_Change = 40
Bullet_State = "Ready"

# Score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

TextX = 10
TextY = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)
win_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def game_win_text():
    winning_text = win_font.render("YOU WIN!", True, (255, 255, 255))
    screen.blit(winning_text, (200, 250))

def player(x, y):
    screen.blit(Player_Image, (x, y))


def enemy(x, y, i):
    screen.blit(Enemy_Image[i], (x, y))


def fire_bullet(x, y):
    global Bullet_State
    Bullet_State = "Fire"
    screen.blit(Bullet_Image, (x + 16, y + 10))


def is_Collision(EnemyX,EnemyY,BulletX,BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True

while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                Player_X_Change = -6
            if event.key == pygame.K_RIGHT:
                Player_X_Change = 6
            if event.key == pygame.K_SPACE and Bullet_State == "Ready":
                bullet_sound = mixer.Sound("audio/laser.wav")
                bullet_sound.play()
                if Bullet_State == "Ready":
                    # Get the x coordinate of the spaceship
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                Player_X_Change = 0

    # Checking for boundaries, ensuring it doesn't go out of boundaries
    PlayerX += Player_X_Change

    # Player Movement
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    win = False

    if score_value == 30:
        win = True

    if win:
        game_win_text()
        pygame.display.update()
        pygame.time.delay(5000)
        quit()

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over 
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            pygame.display.update()
            pygame.time.delay(5000)
            quit()

        EnemyX[i] += Enemy_X_Change[i]
        if EnemyX[i] <= 0:
            Enemy_X_Change[i] = 3
            EnemyY[i] += Enemy_Y_Change[i]
        elif EnemyX[i] >= 736:
            Enemy_X_Change[i] = -3
            EnemyY[i] += Enemy_Y_Change[i]

        # Collision
        collision = is_Collision(EnemyX[i],EnemyY[i],BulletX,BulletY)
        if collision:
            explosion_sound = mixer.Sound("audio/explosion.wav")
            explosion_sound.play()
            BulletY = 480
            Bullet_State = "Ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)

        enemy(EnemyX[i], EnemyY[i], i)

    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_State = "Ready"

    if Bullet_State == "Fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= Bullet_Y_Change
    
    player(PlayerX, PlayerY)
    show_score(TextX, TextY)
    pygame.display.update()