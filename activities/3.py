import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
BULLET_SIZE = 10
ENEMY_SIZE = 40
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell Game")

clock = pygame.time.Clock()

# Load images
player_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_image.fill(WHITE)

bullet_image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
bullet_image.fill(RED)

enemy_image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
enemy_image.fill(BLUE)

# Initialize player
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 10
player_speed = 5

# Initialize bullets
bullets = []

# Initialize enemies
enemies = []

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player input
    keys = pygame.key.get_pressed()
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

    # Spawn enemies
    if random.randint(1, 100) < 2:
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy_y = -ENEMY_SIZE
        enemies.append([enemy_x, enemy_y])

    # Update bullets
    bullets = [[bx, by - 5] for bx, by in bullets if by > 0]

    # Update enemies
    enemies = [[ex, ey + 2] for ex, ey in enemies if ey < HEIGHT]

    # Check for collisions
    for bullet in bullets:
        for enemy in enemies:
            if (
                enemy[0] < bullet[0] < enemy[0] + ENEMY_SIZE
                and enemy[1] < bullet[1] < enemy[1] + ENEMY_SIZE
            ):
                bullets.remove(bullet)
                enemies.remove(enemy)

    # Draw everything
    screen.fill((0, 0, 0))
    screen.blit(player_image, (player_x, player_y))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
