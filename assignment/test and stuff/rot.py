import pygame
screen_height = 560
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))

fis = pygame.image.load("pictures/fish1.png")

e = True
while e:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            e = False
    rot_img = pygame.transform.rotate(fis, 45)
    screen.blit(rot_img, (500, 200))
    pygame.display.update()