import pygame
import random

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
img = pygame.image.load("assignment/the guy.png")

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a surface for the game elements
game_surface = pygame.Surface((WIDTH, HEIGHT))

# Game loop
running = True
shake = False
shake_duration = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press space to start shaking
                shake = True
                shake_duration = 10  # Shake for 10 frames

    # Clear the game surface
    game_surface.fill(BLACK)

    # Draw something on the game surface here
    pygame.draw.rect(game_surface, (255, 0, 0), pygame.Rect(400, 300, 32, 32))

    # Draw the game surface on the screen with an offset if shaking
    if shake and shake_duration > 0:
        offset = random.randint(-20, 20), random.randint(-20, 20)
        screen.blit(game_surface, offset)
        shake_duration -= 1  # Decrease the shake duration
    else:
        pass
    
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
