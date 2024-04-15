import pygame
import random
import time

#init pygame
pygame.init()

clock = pygame.time.Clock()

#set window size
screen_height = 520
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))

font1 = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 100)

def text(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect()

#buttons
def button(msg, x, y, w, h, inactive_colour, active_colour, action=None):
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()

     #check if mouse is hovering over buttons
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, w, h))
        if click [0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, inactive_colour, (x, y, w, h))

    small_text = pygame.font.SysFont('arial', 20)
    text_surf, text_rect = text(msg, small_text)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(text_surf, text_rect)

#player variables
player_img = pygame.image.load("assignment/pictures/the guy.png")
player_x = 604
player_y = 400
player_speed = 8

#column variables
laser_img = [pygame.image.load("assignment/pictures/laser column0.png"), pygame.image.load("assignment/pictures/laser column1.png"), pygame.image.load("assignment/pictures/laser column2.png"), pygame.image.load("assignment/pictures/laser column3.png")]
column_width = 32
column_height = screen_height
lasernum = 0
hlaser_img = [pygame.image.load("assignment/pictures/laser0.png"), pygame.image.load("assignment/pictures/laser1.png"), pygame.image.load("assignment/pictures/laser2.png"), pygame.image.load("assignment/pictures/laser3.png")]
hcolumn_width = screen_width
hcolumn_height = 32
columns = []
hcolumns = []

#bomb variables
bombnum = 0
bomb_secs = pygame.time.get_ticks()
bomb_pic = pygame.image.load(f"assignment/pictures/bomb{bombnum}.png")

#time tracking
column_seconds = pygame.time.get_ticks()

running = True
#main game loop
while running:
    timer = pygame.time.get_ticks()

    if timer - column_seconds > 2000:
        for i in range(2):  
            hcolumns.append([0, random.randint(0, screen_height - hcolumn_height), pygame.time.get_ticks()]) # add a column at a random x position with current time
            Column_seconds = pygame.time.get_ticks() # reset timer

    if timer - column_seconds > 2000:
        for i in range(3): 
            columns.append([random.randint(0, screen_width - column_width), 0, pygame.time.get_ticks()]) # add a column at a random x position with current time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #movement
    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_1]:
        player_speed = 2
    if keypress[pygame.K_2]:
        player_speed = 8
    if keypress[pygame.K_LEFT]:
        player_x -= player_speed
        if player_x <= 0:
            player_x += player_speed
    if keypress[pygame.K_RIGHT]:
        player_x += player_speed
        if player_x >= screen_width - 32:
            player_x -= player_speed
    if keypress[pygame.K_UP]:
        player_y -= player_speed
        if player_y <= 70:
            player_y += player_speed
    if keypress[pygame.K_DOWN]:
        player_y += player_speed
        if player_y >= screen_height - 32:
            player_y -= player_speed

    #draw columns and check for collision
    screen.fill((0, 0, 0))

    for column in columns:
        column_seconds = (pygame.time.get_ticks() - column[2]) / 1000
        if column_seconds < 1: # column is harmless for 1 second
            column_color = (255, 255, 0)
            pygame.draw.rect(screen, column_color, pygame.Rect(column[0], column[1], column_width, column_height))
        elif column_seconds < 3: # column is harmful for next 2 seconds
            column_color = (255, 0, 0)
            pygame.draw.rect(screen, column_color, pygame.Rect(column[0], column[1], column_width, column_height))
            screen.blit(laser_img[lasernum], (column[0], column[1]))
            if lasernum < 3:
                lasernum += 1
            else:
                lasernum = 0
            if column[0] < player_x + 32 and column[0] + column_width > player_x and column[1] < player_y + 32 and column[1] + column_height > player_y:
                print(timer/1000)
                running = False # end the game if the player collides with a column
        else: # remove column after 3 seconds
            columns.remove(column)

    for hcolumn in hcolumns:
        hcolumn_seconds = (pygame.time.get_ticks() - hcolumn[2]) / 1000
        if hcolumn_seconds < 1: # column is harmless for 1 second
            hcolumn_color = (255, 255, 0)
            pygame.draw.rect(screen, hcolumn_color, pygame.Rect(hcolumn[0], hcolumn[1], hcolumn_width, hcolumn_height))
        elif hcolumn_seconds < 3: # column is harmful for next 2 seconds
            hcolumn_color = (255, 0, 0)
            pygame.draw.rect(screen, hcolumn_color, pygame.Rect(hcolumn[0], hcolumn[1], hcolumn_width, hcolumn_height))
            screen.blit(hlaser_img[lasernum], (hcolumn[0], hcolumn[1]))
            if hcolumn[0] < player_x + 32 and hcolumn[0] + hcolumn_width > player_x and hcolumn[1] < player_y + 32 and hcolumn[1] + hcolumn_height > player_y:
                print(timer/1000)
                running = False # end the game if the player collides with a column
        else: # remove column after 3 seconds
            hcolumns.remove(hcolumn)
    
    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 32, 32))
    screen.blit(player_img, (player_x, player_y))
    screen.blit(bomb_pic, (400, 100))
    bombnum += 1
    screen.blit(font1.render(f"Time: {timer/1000}", True, (255, 0, 0)), (0, 460))
    button("quit?", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), quit)
    pygame.display.update()
    clock.tick(60)
print("end")
pygame.quit()