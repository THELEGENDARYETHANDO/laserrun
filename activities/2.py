import pygame
import random

pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Colors
black = (000, 000, 000)
white = (255, 255, 255)
red = (255, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 30)
        self.rect.y = random.randint(0, screen_height - 30)
        self.speed = 3  # Adjust the speed as needed

    def update(self, player_rect):
        # Move towards the player
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player_rect.y:
            self.rect.y -= self.speed

# Create player and enemy objects
player = Player(screen_width // 2 - 25, screen_height // 2 - 25)
enemy = Enemy()

all_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.rect.x = mouse_x
    player.rect.y = mouse_y

    # Update the enemy to follow the player
    enemy.update(player.rect)

    # Draw everything
    screen.fill(white)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
