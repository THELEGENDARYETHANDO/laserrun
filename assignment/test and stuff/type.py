import pygame
import sys

pygame.init()

# Set up the Pygame window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Type and Display Letters")

# Initialize variables
input_text = ""
font = pygame.font.Font(None, 36)
text_color = (0, 0, 0)
name = ""

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif len(input_text) < 3:
                input_text += event.unicode
            name += event.unicode
            print(name)

    screen.fill((255, 255, 255))
    text_surface = font.render(input_text, True, text_color)
    screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, screen_height // 2))
    pygame.display.flip()

pygame.quit()
sys.exit()
