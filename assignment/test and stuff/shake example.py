import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rotating Squares")
clock = pygame.time.Clock()

# Function to draw a rotated square
def draw_rotated_square(x, y, size, angle):
    square = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(square, RED, (0, 0, size, size))
    rotated_square = pygame.transform.rotate(square, angle)
    rotated_rect = rotated_square.get_rect(center=(x, y))
    screen.blit(rotated_square, rotated_rect)

# Main game loop
def main():
    squares = [{'x': random.randint(0, SCREEN_WIDTH), 'y': random.randint(0, SCREEN_HEIGHT),
                'size': 50, 'angle': 0} for _ in range(5)]  # Adjust the number of squares with 'w'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Rotate the screen by a random amount left or right
                    angle = random.uniform(-10, 10)
                    screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                    for square in squares:
                        square['x'], square['y'] = rotate_point(square['x'], square['y'], angle, screen_center)

        screen.fill((255, 255, 255))  # Fill the background with white

        for square in squares:
            draw_rotated_square(square['x'], square['y'], square['size'], square['angle'])

        pygame.display.flip()
        clock.tick(60)

def rotate_point(x, y, angle, center):
    # Rotate a point (x, y) around a center point by a given angle
    angle_rad = math.radians(angle)
    x_rot = center[0] + (x - center[0]) * math.cos(angle_rad) - (y - center[1]) * math.sin(angle_rad)
    y_rot = center[1] + (x - center[0]) * math.sin(angle_rad) + (y - center[1]) * math.cos(angle_rad)
    return x_rot, y_rot

if __name__ == "__main__":
    main()
