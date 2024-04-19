import pygame
pygame.mixer.init()

def fish():
    vine_boom = pygame.mixer.Sound("assignment\sound/vine.mp3")
    pygame.mixer.Sound.play(vine_boom)
    return(pygame.image.load("assignment/pictures/fish1.png"))