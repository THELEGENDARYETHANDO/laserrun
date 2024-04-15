import pygame

fish_rarity = 1
fish_caught = "no fish"
fish1 = pygame.image.load("assignment\pictures/fish1.png")

def fish():
    global fish_caught#, fish_rarity
    #fish_rarity = random.randint(1, 100)
    #if fish_rarity > 90:
    fish_caught = fish1