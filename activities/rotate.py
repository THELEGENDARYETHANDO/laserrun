import pygame
import math

# Load the image
image = pygame.image.load('assignment/snel.png')

screen_height = 520
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))

# Rotate the image
angle = 45  # The rotation angle in degrees
rotated_image = pygame.transform.rotate(image, angle)
e=True
# Now you can draw the rotated image to the screen
while e:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            e = False
    screen.blit(rotated_image, (500, 200))
    pygame.display.flip()
