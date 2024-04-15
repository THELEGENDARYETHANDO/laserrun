#import things
import pygame
import random
import time

#init pygame
pygame.init()

clock = pygame.time.Clock()

#set window size
screen_height = 520
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))

#player data
player_img = pygame.image.load("assignment\pictures/the guy.png")
player_x = 604
player_y = 400
player_speed = 8
tickbase = 0

#set up hazards
class Hazard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 520))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 32)
        self.rect.y = 0
        self.time_created = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.time_created > 1000:
            self.kill()

    def hit(self, player_x, player_y):
        if pygame.Rect(player_x, player_y, 32, 32).colliderect(hazards.rect):
            pygame.quit()

ADDHAZARD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDHAZARD, 1000)

hazards = pygame.sprite.Group()

running = True
#main game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDHAZARD:
            hazards.add(Hazard())

    #movement
    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_LEFT]:
        player_x -= player_speed
        if player_x <= 0:
            player_x += player_speed
    if keypress[pygame.K_RIGHT]:
        player_x += player_speed
        if player_x >= screen_width - 32:
            player_x -= player_speed
    if keypress[pygame.K_UP]:
        player_y -= player_speed
        if player_y <= 0:
            player_y += player_speed
    if keypress[pygame.K_DOWN]:
        player_y += player_speed
        if player_y >= screen_height - 32:
            player_y -= player_speed

    screen.fill(000000)
    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 32, 32))
    screen.blit(player_img, (player_x, player_y))
    hazards.update()
    for hazard in hazards:
        screen.blit(hazard.image, (hazard.rect.x, hazard.rect.y))
    pygame.display.update()
    clock.tick(60)
print("end")
pygame.quit()