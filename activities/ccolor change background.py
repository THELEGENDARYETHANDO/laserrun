import pygame

pygame.init()

clock = pygame.time.Clock()

#Set window size
screen_height = 520
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))

play = True
tickbase = 0

colorswap = [(255, 000, 000), (000, 255, 000), (000, 000, 255)]
x = 0

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    ticks = pygame.time.get_ticks()

    screen.fill(colorswap[x])
    if ticks - tickbase == 1000:
        if x < 2:
            x += 1
        else:
            x = 0
        tickbase = ticks

    pygame.display.update()