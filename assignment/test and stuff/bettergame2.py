import pygame
import random
import time

#init pygame
pygame.init()

clock = pygame.time.Clock()

#set window size
screen_height = 560
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))
surface = pygame.Surface((screen_width, screen_height))
rot_surface = pygame.transform.rotate(surface, 0)
title_img = pygame.image.load("assignment\pictures\Comp Sci game title screen.png")

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
        pygame.draw.rect(surface, active_colour, (x, y, w, h))
        if click [0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(surface, inactive_colour, (x, y, w, h))

    small_text = pygame.font.SysFont('arial', 20)
    text_surf, text_rect = text(msg, small_text)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    surface.blit(text_surf, text_rect)

def start():
    global playing, title, start_time, bomb_spawn_seconds, laser_seconds, bomb_img_seconds, laser_img_seconds
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
    bomb_spawn_seconds = 0
    bomb_img_seconds = 0
    laser_seconds = 0
    laser_img_seconds = 0

def restart():
    global title, death
    title = True
    death = False

#player variables
player_img = pygame.image.load("assignment/pictures/the guy.png")
player_x = 604
player_y = 400
player_speed = 8
start_time = 0

#column variables
laser_img = [pygame.image.load("assignment/pictures/laser column0.png"), pygame.image.load("assignment/pictures/laser column1.png"), pygame.image.load("assignment/pictures/laser column2.png"), pygame.image.load("assignment/pictures/laser column3.png")]
laser_width = 32
laser_height = screen_height
lasernum = 0
hlaser_img = [pygame.image.load("assignment/pictures/laser0.png"), pygame.image.load("assignment/pictures/laser1.png"), pygame.image.load("assignment/pictures/laser2.png"), pygame.image.load("assignment/pictures/laser3.png")]
hlaser_width = screen_width
hlaser_height = 32
laser_img_seconds = 0
laser_seconds = 0
lasers = []
hlasers = []

#bomb variables
bomb_num = 0
bomb_spawn_seconds = 0
bomb_img_seconds = 0
bombs = []
screen_shake = False

title = True
playing = False
death = False
running = True
#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if title:
        screen.blit(surface, (0, 0))
        surface.blit(title_img, (0, 0))
        button("START", screen_width - 272, screen_height - 102, 240, 70,(100, 100, 100), (200, 200, 200), start)
        button("QUIT", 32, screen_height - 102, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        pygame.display.update()

    if playing:
        screen.blit(rot_surface, (0, 0))
        timer = pygame.time.get_ticks()
        play_time = timer - start_time
        
        if play_time - laser_seconds > 3000:
            for i in range((play_time)//10000 + 1):  
                hlasers.append([0, random.randint(0, screen_height - hlaser_height), pygame.time.get_ticks()]) # add a column at a random x position with current time

        if play_time - laser_seconds > 3000:
            for i in range((play_time) // 7000 + 1): 
                lasers.append([random.randint(0, screen_width - laser_width), 0, pygame.time.get_ticks()]) # add a column at a random x position with current time
            laser_seconds = timer - start_time

        #movement
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_1]:
            player_speed = 2
        if keypress[pygame.K_2]:
            player_speed = 8
        if keypress[pygame.K_LEFT]:
            player_x -= player_speed
            if player_x <= 0 - player_speed:
                player_x += player_speed
        if keypress[pygame.K_RIGHT]:
            player_x += player_speed
            if player_x >= screen_width - 20 + player_speed:
                player_x -= player_speed
        if keypress[pygame.K_UP]:
            player_y -= player_speed
            if player_y <= 0 - player_speed:
                player_y += player_speed
        if keypress[pygame.K_DOWN]:
            player_y += player_speed
            if player_y >= screen_height - 32 + player_speed:
                player_y -= player_speed

        surface.fill((50, 50, 50))
        #screen.fill((255, 255, 255))

        #draw lasers and check for collision
        if play_time - laser_img_seconds > 50:
            if lasernum < 3:
                lasernum += 1
                laser_img_seconds = timer - start_time
            else:
                lasernum = 0
                laser_img_seconds = timer - start_time
        for laser in lasers:
            laser_life = (pygame.time.get_ticks() - laser[2]) / 1000
            if laser_life < 1: # column is harmless for 1 second
                laser_color = (255, 255, 0)
                pygame.draw.rect(surface, laser_color, pygame.Rect(laser[0], laser[1], laser_width, laser_height))
            elif laser_life < 3: # column is harmful for next 2 seconds
                surface.blit(laser_img[lasernum], (laser[0], laser[1]))
                if laser[0] < player_x + 20 and laser[0] + laser_width > player_x and laser[1] < player_y + 32 and laser[1] + laser_height > player_y:
                    print((play_time)/1000)
                    death = True
                    playing = False
            else: # remove column after 3 seconds
                lasers.remove(laser)

        for hlaser in hlasers:
            hlaser_life = (pygame.time.get_ticks() - hlaser[2]) / 1000
            if hlaser_life < 1: # column is harmless for 1 second
                hlaser_color = (255, 255, 0)
                pygame.draw.rect(surface, hlaser_color, pygame.Rect(hlaser[0], hlaser[1], hlaser_width, hlaser_height))
            elif hlaser_life < 3: # column is harmful for next 2 seconds
                surface.blit(hlaser_img[lasernum], (hlaser[0], hlaser[1]))
                if hlaser[0] < player_x + 20 and hlaser[0] + hlaser_width > player_x and hlaser[1] < player_y + 32 and hlaser[1] + hlaser_height > player_y:
                    print((play_time)/1000)
                    death = True
                    playing = False
            else: # remove column after 3 seconds
                hlasers.remove(hlaser)

        #pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 20, 32))
        surface.blit(player_img, (player_x, player_y))

        if play_time - bomb_spawn_seconds > 2500:
            for i in range(2):
                bombs.append([random.randint(-112, screen_width - 144), random.randint(-112, screen_height - 144)])
            bomb_spawn_seconds = play_time
            bomb_num = 0
        for bomb in bombs:
            bomb_pic = pygame.image.load(f"assignment/pictures/bomb{bomb_num}.png")
            surface.blit(bomb_pic, (bomb[0], bomb[1]))
            if play_time - bomb_img_seconds > 250:
                screen_shake = True
                if bomb_num < 9:
                    bomb_num += 1
                    bomb_img_seconds = play_time
                else:
                    bombs.remove(bomb)
            if bomb_num >= 7 and bomb[0] < player_x + 20 and bomb[0] + 256 > player_x and bomb[1] < player_y + 32 and bomb[1] + 256 > player_y:
                death = True
                playing = False
        if screen_shake == True:
            if bomb_num >= 6:
                rot_surface = pygame.transform.rotate(surface, random.uniform(-2, 2))
                screen_shake = False
            else:
                rot_surface = pygame.transform.rotate(surface, 0)
        surface.blit(font1.render(f"Time: {(play_time)/1000}", True, (255, 0, 0)), (0, screen_height - 60))
        #button("QUIT", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        pygame.display.update()
        clock.tick(60)

    if death:
            screen.blit(surface, (0, 0))
            surface.fill(000000)
            button("Back to Title", (screen_width-240)/2, (screen_height - 70)/2, 240, 70, (100, 100, 100), (200, 200, 200), restart)
            for bomb in bombs:
                bombs.remove(bomb)
            for laser in lasers:
                lasers.remove(laser)
            for hlaser in hlasers:
                hlasers.remove(hlaser)
            pygame.display.update()
print("end")
pygame.quit()