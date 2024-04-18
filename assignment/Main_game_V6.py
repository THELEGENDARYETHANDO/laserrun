import pygame
import pygame.gfxdraw
import sys
import random
import fish_game
import classes
import movement
import math

#init pygame
pygame.init()
clock = pygame.time.Clock()

#colours
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
transparent_yellow = (255, 255, 0, 100)
invisible = (0, 0, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
light_grey = (200, 200, 200)
grey = (100, 100, 100)

#set window size
screen_height = 560
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))
#Makes a sepperate screen to make screenshake easier
surface = pygame.Surface((screen_width, screen_height))
surface_rotation = 0
#loads some background pictures
title_background = pygame.image.load("assignment/pictures/Comp Sci game title screen.png")
background = pygame.image.load("assignment/pictures/Comp sci background.png")

font = pygame.font.Font(None, 30)

#buttons
def text(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()

def button(message, x, y, w, h, inactive_colour, active_colour, action):
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()

    #check if mouse is hovering over buttons and triggers the action if the mouse is clicked
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(surface, active_colour, (x, y, w, h))
        if click [0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(surface, inactive_colour, (x, y, w, h))

    #makes the text written on the button centered
    font = pygame.font.SysFont(None, 30)
    text_surf, text_rect = text(message, font)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    surface.blit(text_surf, text_rect)

#Functions for changing game states
def start():
    global playing, title, start_time
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
def start_bomb_mayhem():
    global playing, title, start_time, bomb_mayhem
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
    bomb_mayhem = True
def Back_to_title():
    global title, death
    title = True
    death = False
def start_fish():
    global title, fishing
    title = False
    fishing = True
def stop_fish():
    global title, fishing
    title = True
    fishing = False
def go_to_leaderboard():
    global title, leaderboard
    title = False
    leaderboard = True
def leave_leadeboard():
    global title, leaderboard
    title = True
    leaderboard = False
def unpause():
    global pause, playing
    pause = False
    playing = True

#player variables
player_img = pygame.image.load("assignment/pictures/the guy.png")
stamina = 100
player_x = 604
player_y = 400
death_msg = ""
play_time = 0
pause_time = 0
jump_time = 0
name = ""
can_update = False
update = False
#Dictionaries to hold leaderboard values
leaderboard_dict = {1: 0, "name1": "",
               2: 0, "name2": "",
               3: 0, "name3": "",
               4: 0, "name4": "",
               5: 0, "name5": "",
               6: 0, "name6": "",
               7: 0, "name7": "",
               8: 0, "name8": "",
               9: 0, "name9": "",
               10: 0, "name10": ""
               }
bomb_leaderboard_dict = {1: 0, "name1": "",
               2: 0, "name2": "",
               3: 0, "name3": "",
               4: 0, "name4": "",
               5: 0, "name5": "",
               6: 0, "name6": "",
               7: 0, "name7": "",
               8: 0, "name8": "",
               9: 0, "name9": "",
               10: 0, "name10": ""
               }

#Functions to update and display dictionaries
def display_leaderboard(dict, x):
    y = 120
    for i in range(10):
            if dict[i+1] == 0:
                surface.blit(font.render("score = N/A", True, blue), (x, y))
            else:
                surface.blit(font.render(f"score = {dict[i+1] / 1000} seconds by {dict[f'name{i+1}']}", True, blue), (x, y))
            i += 1
            y += 40
def update_leaderboard(score, dict, name):
    for i in range(10):
        if score > dict[i+1]:
            score, dict[i+1] = dict[i+1], score
            dict[f"name{i+1}"], name = name, dict[f"name{i+1}"]

#initialise game states
running = True
title = True
playing = False
death = False
bomb_mayhem = False
leaderboard = False
pause = False
fishing = False
jump = False

#Initialise classes
laser = classes.Laser()
hori_laser = classes.Horizontal_Laser()
vert_laser = classes.Vertical_Laser()
bomb = classes.Bombs()

#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and death == True:
            if event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif event.key == pygame.K_RETURN and can_update == True:
                update = True
                can_update = False
            elif len(name) < 3:
                name += event.unicode
            print(name)

    if title:
        play_time = 0
        bomb_mayhem = False
        screen.blit(surface, (0, 0))
        surface.blit(title_background, (0, 0))
        #renders all the buttons
        button("The Mystery Button", 500, 0, 240, 32, grey, light_grey, start_fish)
        button("START", screen_width - 272, screen_height - 102, 240, 70, grey, light_grey, start)
        button("Bomb Mayhem", screen_width - 512, screen_height - 102, 240, 70, grey, light_grey, start_bomb_mayhem)
        button("Leaderboard", screen_width - 272, 32, 240, 70, grey, light_grey, go_to_leaderboard)
        button("QUIT", 32, screen_height - 102, 240, 70, grey, light_grey, quit)

    if leaderboard:
        screen.blit(surface, (0, 0))
        surface.fill(black)
        #displays the leaderboards
        surface.blit(font.render("Leaderboard", True, red), (200, 80))
        display_leaderboard(leaderboard_dict, 200)
        surface.blit(font.render("Bomb Mayhem Leaderboard", True, red), (600, 80))
        display_leaderboard(bomb_leaderboard_dict, 600)
        button("back to title", 0, 0, 240, 70, grey, light_grey, leave_leadeboard)

    if fishing:
        screen.blit(surface, (0, 0))
        keypress = pygame.key.get_pressed()
        surface.fill(blue)
        surface.blit(font.render("Press f to fish", True, red), (screen_width // 2 - font.render("Press f to fish", True, red).get_width() // 2, 100))
        if keypress[pygame.K_f]:
            surface.blit(fish_game.fish(), (screen_width/2 - 32, screen_height/2 - 16))
        button("Stop fishing :(", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), stop_fish)

    if playing:
        rot_surface = pygame.transform.rotate(surface, surface_rotation)
        screen.blit(rot_surface, (0, 0))
        surface.blit(background, (0, 0))
        #Handles how long you've been playing for.
        timer = pygame.time.get_ticks()
        play_time = timer - start_time - pause_time

        keypress = pygame.key.get_pressed()

        #Lets you jump over lasers
        if keypress[pygame.K_SPACE] and jump == False:
            jump_time = pygame.time.get_ticks()
            jump = True
            player_img = pygame.image.load("assignment/pictures/the guy jump.png")
        #makes sure you can't stay in the air forever.
        if timer - jump_time > 500:
            jump = False
            player_img = pygame.image.load("assignment/pictures/the guy.png")

        #Makes sure the lasers don't spawn if your playing bomb mayhem
        if bomb_mayhem != True:

            #Spawns the lasers on the screen and determines if they are harmful or not
            hori_laser.spawn(play_time)
            hori_laser.attack(play_time, surface, transparent_yellow, player_y, jump)
            vert_laser.spawn(play_time)
            vert_laser.attack(play_time, surface, transparent_yellow, player_x, jump)

        #Spawns and displays bombs
        bomb.spawn(play_time, bomb_mayhem)
        bomb.attack(play_time, player_x, player_y, surface)
        surface.blit(player_img, (player_x, player_y))
        player_x, player_y, stamina = movement.move(player_x, player_y, stamina, surface, yellow)
        #If you get hit by a laser prepares everthing for entering the death screen
        if hori_laser.hit or vert_laser.hit:
            pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (0, 0, 0, 200))
            pygame.image.save(surface, "assignment/pictures/screenshot.png")
            death_img = pygame.image.load("assignment/pictures/screenshot.png")
            death_msg = "Death by laser"
            playing = False
            death = True
            can_update = True
            name = ""
        #Same as above but for bombs
        elif bomb.hit:
            pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (0, 0, 0, 200))
            pygame.image.save(surface, "assignment/pictures/screenshot.png")
            death_img = pygame.image.load("assignment/pictures/screenshot.png")
            death_msg = "Death by bomb"
            playing = False
            death = True
            can_update = True
            name = ""

        #Makes the screen shake if a bomb is exploding
        try:
            if bomb.array[0][2] >= 6:
                surface_rotation = random.uniform(-0.5, 0.5)
        except:
            surface_rotation = 0
        #displays how long you've been alive for
        surface.blit(font.render(f"Time: {(play_time)/1000}", True, red), (0, screen_height - 60))
        #lets you pause the game
        if keypress[pygame.K_ESCAPE]:
            pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (0, 0, 0, 200))
            playing = False
            pause = True

    if pause:
        screen.blit(surface, (0, 0))
        #Makes sure the game knows how long you have been paused for
        pause_time = pygame.time.get_ticks() - play_time - start_time
        button("RESUME", 500, 200, 240, 70, (100, 100, 100), (200, 200, 200), unpause)
        button("QUIT", 500, 400, 240, 70, (100, 100, 100), (200, 200, 200), quit)

    if death:
        screen.blit(surface, (0, 0))
        #lets you see the frame that you died in.
        surface.blit(death_img, (0, 0))
        #checks if you have enteres 3 letters for your name and updates the leaderboard
        if len(name) == 3 and update == True:
            if bomb_mayhem != True:
                update_leaderboard(play_time, leaderboard_dict, name)
            else:
                update_leaderboard(play_time, bomb_leaderboard_dict, name)
            update = False
        #resets lasers and bombs so they are not present when you play again
        bomb.reset()
        vert_laser.reset()
        hori_laser.reset()
        pause_time = 0
        
        #centres all text and displays them
        text1_rect = screen_width // 2 - font.render("Enter your name", True, red).get_width() // 2
        surface.blit(font.render("Enter your name", True, red), (text1_rect, 150))
        text2_rect = screen_width // 2 - font.render(name, True, red).get_width() // 2
        surface.blit(font.render(name, True, red), (text2_rect, 200))
        text3_rect = screen_width // 2 - font.render(death_msg, True, red).get_width() // 2
        surface.blit(font.render(death_msg, True, red), (text3_rect, 100))
        text4_rect = screen_width // 2 - font.render(f"you survived for {play_time/1000} seconds", True, red).get_width() // 2
        surface.blit(font.render(f"you survived for {play_time/1000} seconds", True, red), (text4_rect, 400))
        button("Back to Title", (screen_width - 240)/2, (screen_height - 70)/2, 240, 70, (100, 100, 100), (200, 200, 200), Back_to_title)

    pygame.display.set_caption(f"{int(clock.get_fps())}")
    #updates the display
    pygame.display.update()
    clock.tick(30)
print("end")
pygame.quit()
sys.exit()