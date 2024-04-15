import pygame
import time
import random
#init pygame
pygame.init()

clock = pygame.time.Clock()

#set window size
screen_height = 520
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))

#player data
player_img = pygame.image.load("assignment/the guy.png")
player_x = 604
player_y = 400
player_speed = 8

#set up hazards
#set up hazards
class Hazard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 520))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 32)
        self.rect.y = 0
        self.time_created = pygame.time.get_ticks()  # Record the time when the hazard is created

    def update(self):
        if pygame.time.get_ticks() - self.time_created > 1000:  # If 1 second has passed
            self.kill()  # Remove the hazard

# Create a custom event for adding a new hazard
ADDHAZARD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDHAZARD, 1000)  # 1000 milliseconds = 1 second

hazards = pygame.sprite.Group()

running = True
#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDHAZARD:  # A new hazard should be added
            hazards.add(Hazard())

    #movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        if player_x <= 0:
            player_x += player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        if player_x >= screen_width - 32:
            player_x -= player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
        if player_y <= 0:
            player_y += player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
        if player_y >= screen_height - 32:
            player_y -= player_speed
    
    hazards.update()  # Update all hazards

    screen.fill(000000)
    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 32, 32))
    screen.blit(player_img, (player_x, player_y))
    for hazard in hazards:
        screen.blit(hazard.image, (hazard.rect.x, hazard.rect.y))
    pygame.display.update()
    clock.tick(60)
print("end")
pygame.quit()
