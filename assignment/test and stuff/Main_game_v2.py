import pygame
import pygame.gfxdraw
import random
#import fish_game
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
title_img = pygame.image.load("assignmentpictures\Comp Sci game title screen.png")
background = pygame.image.load("assignmentpictures\Comp sci background.png")

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
    global playing, title, start_time, bomb_spawn_seconds, laser_seconds, hlaser_seconds, bomb_img_seconds, laser_img_seconds
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
    bomb_spawn_seconds = 0
    bomb_img_seconds = 0
    laser_seconds = 0
    hlaser_seconds = 0
    laser_img_seconds = 0

def Back_to_title():
    global title, death
    title = True
    death = False

#player variables
player_img = pygame.image.load("assignmentpictures/the guy.png")
player_x = 604
player_y = 400
player_speed = 8
start_time = 0
death_msg = "DEATH"
best_time = 0.0
play_time = 0

#column variables
laser_img = [pygame.image.load("assignmentpictures/laser column0.png"), pygame.image.load("assignmentpictures/laser column1.png"), pygame.image.load("assignmentpictures/laser column2.png"), pygame.image.load("assignmentpictures/laser column3.png")]
laser_width = 32
laser_height = screen_height
lasernum = 0
hlaser_img = [pygame.image.load("assignmentpictures/laser0.png"), pygame.image.load("assignmentpictures/laser1.png"), pygame.image.load("assignmentpictures/laser2.png"), pygame.image.load("assignmentpictures/laser3.png")]
hlaser_width = screen_width
hlaser_height = 32
laser_img_seconds = 0
laser_seconds = 0
hlaser_seconds = 0
lasers = []
hlasers = []

#bomb variables
bomb_num = 0
bomb_spawn_seconds = 0
bomb_img_seconds = 0
bombs = []

title = True
playing = False
death = False
running = True
#fish_game.fishing = False
#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if title:
        if play_time > best_time:
            best_time = play_time
        screen.blit(surface, (0, 0))
        surface.blit(title_img, (0, 0))
        surface.blit(font1.render(f"Best time = {best_time/1000} seconds!", True, (0, 0, 0)), (screen_width - 300, screen_height - 20))
#        button("The Mystery Button", 500, 0, 240, 70,(100, 100, 100), (200, 200, 200), fish_game.start_fish)
        button("START", screen_width - 272, screen_height - 102, 240, 70,(100, 100, 100), (200, 200, 200), start)
        button("QUIT", 32, screen_height - 102, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        pygame.display.update()

#    if fish_game.fishing:
#        title = False
#        screen.blit(surface, (0, 0))
#        keypress = pygame.key.get_pressed()
#        surface.fill((0, 0, 255))
#        fish_game.fish()
#        if keypress[pygame.K_f]:
#            surface.blit(fish_game.fish_caught, (screen_width/2 - 32, screen_height/2 - 16))
#        pygame.display.update()

    if playing:
        screen.blit(rot_surface, (0, 0))
        timer = pygame.time.get_ticks()
        play_time = timer - start_time
        
        if play_time - hlaser_seconds > 3000:
            for i in range((play_time)//10000 + 1):  
                hlasers.append([0, random.randint(0, screen_height - hlaser_height), pygame.time.get_ticks()]) # add a column at a random x position with current time
            hlaser_seconds = timer-start_time

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
            if player_x < 32:
                player_x = screen_width - 52
        if keypress[pygame.K_RIGHT]:
            player_x += player_speed
            if player_x > screen_width - 40:
                player_x = 32
        if keypress[pygame.K_UP]:
            player_y -= player_speed
            if player_y < 32:
                player_y = screen_height - 64
        if keypress[pygame.K_DOWN]:
            player_y += player_speed
            if player_y > screen_height - 64:
                player_y = 32

        rot_surface.blit(background, (0, 0))

        #draw lasers and check for collision
        if play_time - laser_img_seconds > 50:
            if lasernum < 3:
                lasernum += 1
                laser_img_seconds = timer - start_time
            else:
                lasernum = 0
                laser_img_seconds = timer - start_time
        for laser in lasers:
            laser_life = (pygame.time.get_ticks() - laser[2])
            if laser_life < 1000: # column is harmless for 1 second
                laser_color = (255, 255, 0)
                pygame.draw.rect(rot_surface, laser_color, pygame.Rect(laser[0], laser[1], laser_width, laser_height))
            elif laser_life < 3000: # column is harmful for next 2 seconds
                rot_surface.blit(laser_img[lasernum], (laser[0], laser[1]))
                if laser[0] < player_x + 20 and laser[0] + laser_width > player_x and laser[1] < player_y + 32 and laser[1] + laser_height > player_y:
                    print((play_time)/1000)
                    death_msg = "Death by laser"
                    death = True
                    playing = False
            else: # remove column after 3 seconds
                lasers.remove(laser)

        for hlaser in hlasers:
            hlaser_life = (pygame.time.get_ticks() - hlaser[2])
            if hlaser_life < 1000: # column is harmless for 1 second
                pygame.draw.rect(rot_surface, (255, 255, 0), pygame.Rect(hlaser[0], hlaser[1], hlaser_width, hlaser_height))
            elif hlaser_life < 3000: # column is harmful for next 2 seconds
                rot_surface.blit(hlaser_img[lasernum], (hlaser[0], hlaser[1]))
                if hlaser[0] < player_x + 20 and hlaser[0] + hlaser_width > player_x and hlaser[1] < player_y + 32 and hlaser[1] + hlaser_height > player_y:
                    print((play_time)/1000)
                    death_msg = "Death by laser"
                    death = True
                    playing = False
            else: # remove column after 3 seconds
                hlasers.remove(hlaser)

        #pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 20, 32))
        rot_surface.blit(player_img, (player_x, player_y))

        #gets the coulour of the pixel at each corner of the player
        player_pixel_colour1 = screen.get_at((int(player_x), int(player_y)))
        player_pixel_colour2 = screen.get_at((int(player_x + 20), int(player_y)))
        player_pixel_colour3 = screen.get_at((int(player_x), int(player_y + 32)))
        player_pixel_colour4 = screen.get_at((int(player_x + 20), int(player_y + 32)))

        if play_time - bomb_spawn_seconds > 2500:
            for i in range(2):
                bombs.append([random.randint(-112, screen_width - 144), random.randint(-112, screen_height - 144)])
            bomb_spawn_seconds = play_time
            bomb_num = 0
        for bomb in bombs:
            bomb_pic = pygame.image.load(f"assignment/pictures/bomb{bomb_num}.png")
            rot_surface.blit(bomb_pic, (bomb[0], bomb[1]))
            if play_time - bomb_img_seconds > 250:
                if bomb_num < 9:
                    bomb_num += 1
                    bomb_img_seconds = play_time
                else:
                    bombs.remove(bomb)
            #detects if the colour at each corner of the player is one of the coulours used in the bomb explosion
            if bomb_num >= 7 and player_pixel_colour1 == (174, 27, 27) or player_pixel_colour2 == (174, 27, 27) or player_pixel_colour3 == (174, 27, 27) or player_pixel_colour4 == (174, 27, 27) or player_pixel_colour1 == (219, 90, 0) or player_pixel_colour2 == (219, 90, 0) or player_pixel_colour3 == (219, 90, 0) or player_pixel_colour4 == (219, 90, 0) or player_pixel_colour1 == (255, 150, 0) or player_pixel_colour2 == (255, 150, 0) or player_pixel_colour3 == (255, 150, 0) or player_pixel_colour4 == (255, 150, 0):
                #rot_surface = pygame.transform.rotate(rot_surface, random.randint(-1, 1))
                death_msg = "Death by bomb"
                death = True
                playing = False
        rot_surface.blit(font1.render(f"Time: {(play_time)/1000}", True, (255, 0, 0)), (0, screen_height - 60))
        #button("QUIT", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        pygame.display.update()
        clock.tick(60)

    if death:
            screen.blit(surface, (0, 0))
            surface.fill(000000)
            button("Back to Title", (screen_width-240)/2, (screen_height - 70)/2, 240, 70, (100, 100, 100), (200, 200, 200), Back_to_title)
            surface.blit(font1.render(death_msg, True, (255, 0, 0)), (550, 100))
            surface.blit(font1.render(f"you survived for {play_time/1000} seconds", True, (255, 0, 0)), (450, 400))
            for bomb in bombs:
                bombs.remove(bomb)
            for laser in lasers:
                lasers.remove(laser)
            for hlaser in hlasers:
                hlasers.remove(hlaser)
            pygame.display.update()
print("end")
pygame.quit()