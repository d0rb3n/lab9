import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()
FPS = 120
FramePerSec = pygame.time.Clock()

red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SPEED2 = 5 #coin speed
SCORE = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

background = pygame.image.load("road.png")

# Create screen
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(white)
pygame.display.set_caption("Game")


# Enemy car
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("car2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.speed = SPEED  # Initial speed for the enemy car

    def move(self):
        global SCORE
        self.rect.move_ip(0, self.speed)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            # Check if score is a multiple of 10
            if SCORE % 10 == 0:
                self.speed += 0.5  # Increase speed by 0.5 when score is a multiple of 10


# Player car
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("car1.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# Coin
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('coin.png')
        def_img_size = (50, 50)
        self.image = pygame.transform.scale(image, def_img_size)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.speed = SPEED2
    def move(self):
        self.rect.move_ip(0, self.speed)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#coin2 / super
class Coin2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.image.load('coin2.png')
        def_img_size = (50, 50)
        self.image = pygame.transform.scale(image, def_img_size)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.speed = SPEED2
    def move(self):
        self.rect.move_ip(0, self.speed)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Setting up Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()
C2 = Coin2()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
coins2 = pygame.sprite.Group()
coins2.add(C2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(C2)

# Increasing speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# New user event for spawning coins
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_COIN, 5000)

#new user event for spawning super coins
SPAWN_COIN2 = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWN_COIN2, 13000)


# Spawning new coins
def spawn_coin():
    new_coin = Coin()
    coins.add(new_coin)
    all_sprites.add(new_coin)
#spawn super coin
def spawn_coin2():
    new_coin2 = Coin2()
    coins.add(new_coin2)
    all_sprites.add(new_coin2)

# Game Loop
while True:
    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_COIN:
            spawn_coin()
        if event.type == SPAWN_COIN2:
            spawn_coin2()
        if event.type == INC_SPEED:
            SPEED += 0.5

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, white)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Hitting the coin
    if pygame.sprite.spritecollide(P1, coins, True):
        pygame.mixer.Sound('catch.mp3').play()
        SCORE += 5
    
    #hitting the super coin
    if pygame.sprite.spritecollide(P1,coins2, True):
        pygame.mixer.Sound('catch.mp3').play()
        SCORE += 10

    # Hitting the car
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(red)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
