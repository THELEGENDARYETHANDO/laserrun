import pygame
import pygame.gfxdraw
import sys
import random
import fish_game
import math

laser_spawn_time = 0
#init pygame
pygame.init()
clock = pygame.time.Clock()

#colours
red = (255, 0, 0)
blue = (0, 0, 255)
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
surface = pygame.Surface((screen_width, screen_height))
surface_rotation = 0
rot_surface = pygame.transform.rotate(surface, 0)
title_img = pygame.image.load("assignment/pictures/Comp Sci game title screen.png")
background = pygame.image.load("assignment/pictures/Comp sci background.png")

font1 = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 100)

def text(text, font):
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()

#buttons
def button(message, x, y, w, h, inactive_colour, active_colour, action):
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
    text_surf, text_rect = text(message, small_text)
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    surface.blit(text_surf, text_rect)

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

#laser variables
class Laser:
    def __init__(self):
        self.img_time = 0
        self.img_num = 0
    
    def spawn(self, time):
        for i in range(time // 10000 + 1):
            horizontal_laser_coords = Horizontal_Laser.spawn(laser)
            hori_laser.array.append([horizontal_laser_coords, time])
        for i in range(time // 7000 + 1):
            vertical_laser_coords = Vertical_Laser.spawn(laser)
            vert_laser.array.append([vertical_laser_coords, time])

    def animation(self, time):
        if time - self.img_time > 25:
            if self.img_num < 3:
                self.img_num += 1
            else:
                self.img_num = 0
            self.img_time = time

class Horizontal_Laser(Laser):
    def __init__(self):
        super().__init__()
        self.array = []
        self.hit = False

    def attack(self, time):
        for laser in self.array:
            self.life = time - laser[1]
            if self.life < 1000:
                pygame.gfxdraw.box(surface, (0, laser[0], screen_width, 32), transparent_yellow)
            elif self.life < 3000:
                self.animation(play_time)
                self.img = pygame.image.load(f"assignment/pictures/hori_laser{self.img_num}.png")
                surface.blit(self.img, (0, laser[0]))
                if player_y < laser[0] + 32 and player_y + 32 > laser[0] and jump != True:
                    self.hit = True
            else:
                self.array.remove(laser)
    def spawn(self):
        self.width = screen_width
        self.height = 32
        self.y_pos = random.randint(0, screen_height - 32)
        return (self.y_pos)
    
    def reset(self):
        for laser in self.array:
            self.array.remove(laser)
            self.hit = False
            self.img_time = 0

class Vertical_Laser(Laser):
    def __init__(self):
        super().__init__()
        self.array = []
        self.hit = False

    def attack(self, time):
        for laser in self.array:
            self.life = time - laser[1]
            if self.life < 1000:
                pygame.gfxdraw.box(surface, (laser[0], 0, 32, screen_height), transparent_yellow)
            elif self.life < 3000: 
                self.animation(play_time)
                self.img = pygame.image.load(f"assignment/pictures/vert_laser{self.img_num}.png")
                surface.blit(self.img, (laser[0], 0))
                if player_x < laser[0] + 20 and player_x + 20 > laser[0] and jump != True:
                    self.hit = True
            else:
                self.array.remove(laser)

    def spawn(self):
        self.width = 32
        self.height = screen_height
        self.x_pos = random.randint(0, screen_width - 32)
        return (self.x_pos)
    
    def reset(self):
        for laser in self.array:
            self.array.remove(laser)
            self.hit = False
            self.img_time = 0

class Bombs:
    #initialise the bomb class
    def __init__(self):
        self.img_time = 0
        self.img_num = 0
        self.spawn_num = 1
        self.last_spawn_time = 0
        self.spawn_time = 2500
        self.array = []
        self.hit = False

    def spawn(self, time):
        #Determines how many bombs will spawn at a time
        if bomb_mayhem == True:
            self.spawn_num = 1
        else:
            self.spawn_num = 2
        #determines the interval between bomb spawn times (caps out at 100 miliseconds in bomb mayhem)
        if bomb_mayhem == True:
            self.spawn_time = 600 - (time // 100) 
            if self.spawn_time <= 100:
                self.spawn_time = 100
        else:
            self.spawn_time = 2500
        #Appends the bombs into an array to spawn them
        if time - self.last_spawn_time > self.spawn_time:
            for i in range(self.spawn_num):
                self.array.append([random.randint(-112, screen_width - 144), random.randint(-112, screen_height - 144), 0, 0, 128]) # makes sure the bombs always spawn on the screen
            self.last_spawn_time = play_time

    def attack(self, time, x, y):
        for bomb in self.array:
            if bomb[2] == 6:
                bomb[4] = 32
            elif bomb[2] == 7:
                bomb[4] = 64
            elif bomb[2] == 8:
                bomb[4] = 96
            elif bomb[2] >= 9:
                bomb[4] = 128
            if time - bomb[3] > 250:
                if bomb[2] < 11:
                    bomb[2] += 1
                    bomb[3] = time
                else:
                    self.array.remove(bomb)
            bomb_pic = pygame.image.load(f"assignment/pictures/bomb{bomb[2]}.png")
            surface.blit(bomb_pic, (bomb[0], bomb[1]))

            circle_x = bomb[0] + 128
            circle_y = bomb[1] + 128
            circle_r = bomb[4]
            pygame.gfxdraw.filled_circle(surface, circle_x, circle_y, circle_r, invisible)

            # Calculate the closest point on the rectangle to the circle
            closest_x = max(x, min(circle_x, x + 20))
            closest_y = max(y, min(circle_y, y + 32))

            # Calculate the distance between the circle's center and the closest point on the rectangle
            distance = math.sqrt((circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2)

            # Check if the distance is less than the circle's radius
            if distance < circle_r and bomb[2] > 6:
                self.hit = True

    def reset(self):
        for bomb in self.array:
            self.array.remove(bomb)
            self.hit = False
            self.last_spawn_time = 0

#player variables
player_img = pygame.image.load("assignment/pictures/the guy.png")
player_x = 604
player_y = 400
player_speed = 8
start_time = 0
death_msg = ""
best_time = 0.0
bomb_mayhem_best_time = 0.0
play_time = 0
pause_time = 0
jump_time = 0
name = ""
can_update = False
update = False
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


def display_leaderboard(dict, x):
    y = 80
    for i in range(10):
            if dict[i+1] == 0:
                surface.blit(font1.render(f"score = N/A", True, blue), (x, y))
            else:
                surface.blit(font1.render(f"score = {dict[i+1] / 1000} seconds by {dict[f'name{i+1}']}", True, blue), (x, y))
            i += 1
            y += 40

def update_leaderboard(score, dict, name):
    for i in range(10):
        if score > dict[i+1]:
            score, dict[i+1] = dict[i+1], score
            dict[f"name{i+1}"], name = name, dict[f"name{i+1}"]

title = True
playing = False
death = False
running = True
bomb_mayhem = False
leaderboard = False
pause = False
fishing = False
jump = False

laser = Laser()
hori_laser = Horizontal_Laser()
vert_laser = Vertical_Laser()
bomb = Bombs()
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
        surface.blit(title_img, (0, 0))
        surface.blit(font1.render(f"Best time = {best_time/1000} seconds!", True, black), (screen_width - 300, screen_height - 20))
        surface.blit(font1.render(f"Bomb mayhem best time = {bomb_mayhem_best_time/1000} seconds!", True, black), (screen_width - 750, screen_height - 20))
        button("The Mystery Button", 500, 0, 240, 32, grey, light_grey, start_fish)
        button("START", screen_width - 272, screen_height - 102, 240, 70, grey, light_grey, start)
        button("Bomb Mayhem", screen_width - 512, screen_height - 102, 240, 70, grey, light_grey, start_bomb_mayhem)
        button("Leaderboard", screen_width - 272, 32, 240, 70, grey, light_grey, go_to_leaderboard)
        button("QUIT", 32, screen_height - 102, 240, 70, grey, light_grey, quit)
        #pygame.display.update()

    if leaderboard:
        screen.blit(surface, (0, 0))
        surface.fill(black)
        display_leaderboard(leaderboard_dict, 200)
        display_leaderboard(bomb_leaderboard_dict, 600)
        button("back to title", 0, 0, 240, 70, grey, light_grey, leave_leadeboard)

    if fishing:
        screen.blit(surface, (0, 0))
        keypress = pygame.key.get_pressed()
        surface.fill(blue)
        fish_game.fish()
        if keypress[pygame.K_f]:
            surface.blit(fish_game.fish_caught, (screen_width/2 - 32, screen_height/2 - 16))
        button("Stop fishing :(", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), stop_fish)
        #pygame.display.update()

    if playing:
        rot_surface = pygame.transform.rotate(surface, surface_rotation)
        screen.blit(rot_surface, (0, 0))
        timer = pygame.time.get_ticks()
        play_time = timer - start_time - pause_time
        surface.blit(background, (0, 0))

        #movement
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_LSHIFT] or keypress[pygame.K_RSHIFT]:
            player_speed = 16
        else:
            player_speed = 8
        if keypress[pygame.K_LEFT] or keypress[pygame.K_a]:
            player_x -= player_speed
            if player_x < 32:
                player_x = screen_width - 52
        if keypress[pygame.K_RIGHT] or keypress[pygame.K_d]:
            player_x += player_speed
            if player_x > screen_width - 40:
                player_x = 32
        if keypress[pygame.K_UP] or keypress[pygame.K_w]:
            player_y -= player_speed
            if player_y < 32:
                player_y = screen_height - 64
        if keypress[pygame.K_DOWN] or keypress[pygame.K_s]:
            player_y += player_speed
            if player_y > screen_height - 64:
                player_y = 32

        if keypress[pygame.K_SPACE] and jump == False:
            jump_time = pygame.time.get_ticks()
            jump = True
            player_img = pygame.image.load("assignment/pictures/the guy jump.png")
        if timer - jump_time > 500:
            jump = False
            player_img = pygame.image.load("assignment/pictures/the guy.png")

        #Makes sure the lasers don't spawn if your playing bomb mayhem
        if bomb_mayhem != True:
            #Appends the coordinates of lasers that are spawning
            if play_time - laser_spawn_time > 3000:
                laser.spawn(play_time)
                laser_spawn_time = play_time

            #Spawns the lasers on the screen and determines if they are harmful or not
            hori_laser.attack(play_time)
            vert_laser.attack(play_time)

        bomb.spawn(play_time)
        bomb.attack(play_time, player_x, player_y)
        surface.blit(player_img, (player_x, player_y))
        if hori_laser.hit or vert_laser.hit:
            pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (0, 0, 0, 200))
            death_msg = "Death by laser"
            playing = False
            death = True
            can_update = True
            name = ""
        elif bomb.hit:
            pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (0, 0, 0, 200))
            death_msg = "Death by bomb"
            playing = False
            death = True
            can_update = True
            name = ""

        try:
            if bomb.array[0][2] >= 6:
                surface_rotation = random.uniform(-0.5, 0.5)
        except:
            surface_rotation = 0
        surface.blit(font1.render(f"Time: {(play_time)/1000}", True, red), (0, screen_height - 60))
        #button("QUIT", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        if keypress[pygame.K_ESCAPE]:
            pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (0, 0, 0, 200))
            playing = False
            pause = True
        #pygame.display.update()
        clock.tick(60)

    if pause:
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_p]:
            pause = False
            playing = True
        pause_time = pygame.time.get_ticks() - play_time - start_time
        button("QUIT", 500, 400, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        #pygame.display.update()

    if death:
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
        if play_time > best_time and bomb_mayhem == False:
            best_time = play_time
        if play_time > bomb_mayhem_best_time and bomb_mayhem == True:
            bomb_mayhem_best_time = play_time
        pause_time = 0
        laser_spawn_time = 0
        screen.blit(surface, (0, 0))
        #pygame.gfxdraw.box(surface, (0, 0, screen_width, screen_height), (0, 0, 0, 1))
        surface.blit(font1.render(name, True, red), (screen_width // 2 - font1.render(name, True, red).get_width() // 2, 150))
        button("Back to Title", (screen_width - 240)/2, (screen_height - 70)/2, 240, 70, (100, 100, 100), (200, 200, 200), Back_to_title)
        surface.blit(font1.render(death_msg, True, red), (550, 100))
        surface.blit(font1.render(f"you survived for {play_time/1000} seconds", True, red), (450, 400))
        #pygame.display.update()
    pygame.display.update()
print("end")
pygame.quit()
sys.exit()