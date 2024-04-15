import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Bullet Hell")

# Load images
player_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_image.fill(WHITE)

bullet_image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
bullet_image.fill(RED)

# Initialize player
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 10

# Initialize bullets
bullets = []

# Clock to control the frame rate
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player input
    keys = pygame.key.get_pressed()
    player_speed = 5
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - PLAYER_SIZE:
        player_y += player_speed

    # Shooting bullets
    if keys[pygame.K_SPACE]:
        bullet_x = player_x + PLAYER_SIZE // 2 - BULLET_SIZE // 2
        bullet_y = player_y
        bullets.append([bullet_x, bullet_y])

    # Update bullets
    bullets = [[bx - random.randint (-5, 5), by - random.randint(-1, 5)] for bx, by in bullets if by > 0]

    # Draw everything
    screen.fill((0, 0, 0))
    screen.blit(player_image, (player_x, player_y))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    

    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)
