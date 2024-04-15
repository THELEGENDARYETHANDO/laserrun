import pygame
import pygame.gfxdraw
import random
#import fish_game
import time

#init pygame
pygame.init()

clock = pygame.time.Clock()

yellow = (255, 255, 0)
transparent_yellow = (255, 255, 0, 100)

#set window size
screen_height = 560
screen_width = 1240
screen = pygame.display.set_mode((screen_width,screen_height))
surface = pygame.Surface((screen_width, screen_height))
surface_rotation = 0
rot_surface = pygame.transform.rotate(surface, 0)
title_img = pygame.image.load("assignment\pictures\Comp Sci game title screen.png")
background = pygame.image.load("assignment\pictures\Comp sci background.png")

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
    global playing, title, start_time, bomb_spawn_seconds, bomb_img_seconds, laser_spawn_time
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
    laser_spawn_time = 0
    bomb_spawn_seconds = 0
    bomb_img_seconds = 0

def start_bomb_mayhem():
    global playing, title, start_time, bomb_spawn_seconds, bomb_img_seconds, bomb_mayhem
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
    bomb_spawn_seconds = 0
    bomb_img_seconds = 0
    bomb_mayhem = True

def Back_to_title():
    global title, death
    title = True
    death = False

#laser variables
vertical_laser_img = [pygame.image.load("assignment/pictures/laser column0.png"), pygame.image.load("assignment/pictures/laser column1.png"), pygame.image.load("assignment/pictures/laser column2.png"), pygame.image.load("assignment/pictures/laser column3.png")]
horizontal_laser_img = [pygame.image.load("assignment/pictures/laser0.png"), pygame.image.load("assignment/pictures/laser1.png"), pygame.image.load("assignment/pictures/laser2.png"), pygame.image.load("assignment/pictures/laser3.png")]
laser_img_num = 0
laser_img_time = 0
laser_spawn_time = 0
horizontal_laser_array = []
vertical_laser_array = []
class Laser:
    def __init__(self):
        super.__init__

class Horizontal_Laser(Laser):
    def spawn(self):
        self.width = screen_width
        self.height = 32
        self.y_pos = random.randint(0, screen_height - 32)
        return (self.y_pos)

class Veritcal_Laser(Laser):
    def spawn(self):
        self.width = 32
        self.height = screen_height
        self.x_pos = random.randint(0, screen_width - 32)
        return (self.x_pos)

#player variables
player_img = pygame.image.load("assignment/pictures/the guy.png")
player_x = 604
player_y = 400
player_speed = 8
start_time = 0
death_msg = "DEATH"
best_time = 0.0
play_time = 0
jump_time = 0

#bomb variables
bomb_num = 0
bomb_spawn_seconds = 0
bomb_spawn_num = 0
bomb_img_seconds = 0
bombs = []

title = True
playing = False
death = False
running = True
bomb_mayhem = False
#fish_game.fishing = False
jump = False
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
        button("Bomb Mayhem", screen_width - 512, screen_height - 102, 240, 70,(100, 100, 100), (200, 200, 200), start_bomb_mayhem)
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
        rot_surface = pygame.transform.rotate(surface, surface_rotation)
        screen.blit(rot_surface, (0, 0))
        timer = pygame.time.get_ticks()
        play_time = timer - start_time
        surface.blit(background, (0, 0))

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

        if bomb_mayhem != True:
            laser = Laser()
            hori_laser = Horizontal_Laser()
            vert_laser = Veritcal_Laser()
            if play_time - laser_spawn_time > 3000:
                for i in range(play_time // 10000 + 1):
                    horizontal_laser_coords = Horizontal_Laser.spawn(laser)
                    horizontal_laser_array.append([horizontal_laser_coords, pygame.time.get_ticks()])
                    print(horizontal_laser_array)
                for i in range(play_time//7000 + 1):
                    vertical_laser_coords = Veritcal_Laser.spawn(laser)
                    vertical_laser_array.append([vertical_laser_coords, pygame.time.get_ticks()])
                    laser_spawn_time = play_time
            for laser in horizontal_laser_array:
                horizontal_laser_life = (pygame.time.get_ticks() - laser[1])
                if horizontal_laser_life < 1000:
                    pygame.gfxdraw.box(surface, (0, laser[0], screen_width, 32), transparent_yellow)
                elif horizontal_laser_life < 3000:
                    surface.blit(horizontal_laser_img[laser_img_num], (0, laser[0]))
                    if player_y < laser[0] + 32 and player_y + 32 > laser[0] and jump != True:
                        death_msg = "Death by laser"
                        playing = False
                        death = True
                else:
                    horizontal_laser_array.remove(laser)
            for laser in vertical_laser_array:
                vertical_laser_life = (pygame.time.get_ticks() - laser[1])
                if vertical_laser_life < 1000:
                    pygame.gfxdraw.box(surface, (laser[0], 0, 32, screen_height), transparent_yellow)
                elif vertical_laser_life < 3000:
                    surface.blit(vertical_laser_img[laser_img_num], (laser[0], 0))
                    if player_x < laser[0] + 32 and player_x + 32 > laser[0] and jump != True:
                        death_msg = "Death by laser"
                        playing = False
                        death = True
                else:
                    vertical_laser_array.remove(laser)

            if play_time - laser_img_time > 25:
                if laser_img_num < 3:
                    laser_img_num += 1
                else:
                    laser_img_num = 0
                laser_img_time = play_time

        if keypress[pygame.K_SPACE]:
            jump_time = pygame.time.get_ticks()
            jump = True
            player_img = pygame.image.load("assignment\pictures/the guy jump.png")
        if timer - jump_time > 500:
            jump = False
            player_img = pygame.image.load("assignment/pictures/the guy.png")
        surface.blit(player_img, (player_x, player_y))

        #gets the coulour of the pixel at each corner of the player
        player_pixel_colour1 = screen.get_at((int(player_x), int(player_y)))
        player_pixel_colour2 = screen.get_at((int(player_x + 20), int(player_y)))
        player_pixel_colour3 = screen.get_at((int(player_x), int(player_y + 32)))
        player_pixel_colour4 = screen.get_at((int(player_x + 20), int(player_y + 32)))

        if bomb_mayhem == True:
            bomb_spawn_num = (play_time // 5000) + 2
        else:
            bomb_spawn_num = 2

        if play_time - bomb_spawn_seconds > 2500:
            for i in range(bomb_spawn_num):
                bombs.append([random.randint(-112, screen_width - 144), random.randint(-112, screen_height - 144)]) # makes sure the bombs always spawn on the screen
            bomb_spawn_seconds = play_time
            bomb_num = 0
        for bomb in bombs:
            if bomb_num < 6:
                pygame.gfxdraw.filled_circle(surface, bomb[0] + 128, bomb[1] + 128, 150, transparent_yellow)
            bomb_pic = pygame.image.load(f"assignment/pictures/bomb{bomb_num}.png")
            surface.blit(bomb_pic, (bomb[0], bomb[1]))
            if play_time - bomb_img_seconds > 250:
                if bomb_num < 9:
                    bomb_num += 1
                    bomb_img_seconds = play_time
                else:
                    bombs.remove(bomb)
            #detects if the colour at each corner of the player is one of the coulours used in the bomb explosion
            if bomb_num >= 7 and player_pixel_colour1 == (174, 27, 27) or player_pixel_colour2 == (174, 27, 27) or player_pixel_colour3 == (174, 27, 27) or player_pixel_colour4 == (174, 27, 27) or player_pixel_colour1 == (219, 90, 0) or player_pixel_colour2 == (219, 90, 0) or player_pixel_colour3 == (219, 90, 0) or player_pixel_colour4 == (219, 90, 0) or player_pixel_colour1 == (255, 150, 0) or player_pixel_colour2 == (255, 150, 0) or player_pixel_colour3 == (255, 150, 0) or player_pixel_colour4 == (255, 150, 0):
                rot_surface = pygame.transform.rotate(surface, random.randint(-1, 1))
                death_msg = "Death by bomb"
                death = True
                playing = False
        surface.blit(font1.render(f"Time: {play_time/1000}", True, (255, 0, 0)), (0, screen_height - 60))
        #button("QUIT", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        pygame.display.update()
        clock.tick(60)

    if death:
        bomb_mayhem = False
        screen.blit(surface, (0, 0))
        surface.fill(000000)
        button("Back to Title", (screen_width - 240)/2, (screen_height - 70)/2, 240, 70, (100, 100, 100), (200, 200, 200), Back_to_title)
        surface.blit(font1.render(death_msg, True, (255, 0, 0)), (550, 100))
        surface.blit(font1.render(f"you survived for {play_time/1000} seconds", True, (255, 0, 0)), (450, 400))
        for bomb in bombs:
            bombs.remove(bomb)
        for laser in horizontal_laser_array:
            horizontal_laser_array.remove(laser)
        for laser in vertical_laser_array:
            vertical_laser_array.remove(laser)
        pygame.display.update()
print("end")
pygame.quit()