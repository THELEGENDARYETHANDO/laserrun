import pygame
import pygame.gfxdraw
import math

screen_height = 560
screen_width = 1240

#function to allow player to move
def move(x, y, stamina, plane, colour, exhaustion):
    exhaust_drain = 0
    drain = 0
    keypress = pygame.key.get_pressed()
    if stamina > 0:
        #if you hold shift and have more than 0 stamina you get to run fast
        if keypress[pygame.K_LSHIFT] or keypress[pygame.K_RSHIFT]:
            player_speed = 16
            drain = 1
            exhaust_drain = 1
        else:
            player_speed = 8
            if stamina < 100:
                #-math.e**(-0.001*exhaustion) is a complex math equation I use to replicate an exhaustion system, so the more you sprint, the slower you regain stamina
                drain = -math.e**(-0.001*exhaustion)
    else:
        player_speed = 8
        if stamina < 100 and keypress[pygame.K_LSHIFT] != True and keypress[pygame.K_RSHIFT] != True:
            #-math.e**(-0.001*exhaustion) is a complex math equation I use to replicate an exhaustion system, so the more you sprint, the slower you regain stamina
            drain = -math.e**(-0.001*exhaustion)
    #displays your stamina bar on screen
    pygame.gfxdraw.box(plane, (x - 15, y - 10, stamina // 2, 5), colour)
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
    return(x, y, stamina - drain, exhaustion + exhaust_drain)