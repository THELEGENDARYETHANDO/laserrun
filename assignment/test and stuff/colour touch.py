import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Color Detection Example")
clock = pygame.time.Clock()

# Define colors
player_color = (255, 0, 0)  # Red color for the player
target_color = (0, 255, 0)  # Green color for the target

# Set up player
player_size = 50
player_x, player_y = width // 2, height // 2
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

# Set up target
target_size = 50
target_x, target_y = 400, 300
target_rect = pygame.Rect(target_x, target_y, target_size, target_size)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player with arrow keys
    keys = pygame.key.get_pressed()
    player_speed = 5
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Update player rectangle
    player_rect.x = player_x
    player_rect.y = player_y

    # Check if player is touching the target color
    player_pixel_color = screen.get_at((int(player_x), int(player_y)))
    if player_pixel_color == target_color:
        print("Player is touching the target color!")

    # Fill the screen with background color
    screen.fill((255, 255, 255))

    # Draw the player and target
    pygame.draw.rect(screen, player_color, player_rect)
    pygame.draw.rect(screen, target_color, target_rect)
    clock.tick(60)
    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

# Exit the program
sys.exit()
