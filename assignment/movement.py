import pygame

screen_height = 560
screen_width = 1240

#function to allow player to move
def move(x, y):
    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_LSHIFT] or keypress[pygame.K_RSHIFT]:
        player_speed = 16
    else:
        player_speed = 8
    if keypress[pygame.K_LEFT] or keypress[pygame.K_a]:
        x -= player_speed
        if x < 32:
            x = screen_width - 52
    if keypress[pygame.K_RIGHT] or keypress[pygame.K_d]:
        x += player_speed
        if x > screen_width - 40:
            x = 32
    if keypress[pygame.K_UP] or keypress[pygame.K_w]:
        y -= player_speed
        if y < 32:
            y = screen_height - 64
    if keypress[pygame.K_DOWN] or keypress[pygame.K_s]:
        y += player_speed
        if y > screen_height - 64:
            y = 32
    return(x, y)