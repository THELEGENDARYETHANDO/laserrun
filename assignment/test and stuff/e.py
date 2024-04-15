import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Precise Circle-Rectangle Collision")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define circle properties
circle_radius = 50
circle_x, circle_y = width // 2, height // 2

# Define rectangle properties
rect_width, rect_height = 100, 150
rect_x, rect_y = 300, 200

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the rectangle with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect_x -= 5
    if keys[pygame.K_RIGHT]:
        rect_x += 5
    if keys[pygame.K_UP]:
        rect_y -= 5
    if keys[pygame.K_DOWN]:
        rect_y += 5

    # Clear the screen
    screen.fill(WHITE)

    # Draw the circle
    pygame.draw.circle(screen, BLACK, (circle_x, circle_y), circle_radius)

    # Draw the rectangle
    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height))

    # Calculate the center of the circle
    circle_center = (circle_x, circle_y)

    # Calculate the closest point on the rectangle to the circle
    closest_x = max(rect_x, min(circle_center[0], rect_x + rect_width))
    closest_y = max(rect_y, min(circle_center[1], rect_y + rect_height))

    # Calculate the distance between the circle's center and the closest point on the rectangle
    distance = math.sqrt((circle_center[0] - closest_x) ** 2 + (circle_center[1] - closest_y) ** 2)

    # Check if the distance is less than the circle's radius
    if distance < circle_radius:
        print("Collision detected!")

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
