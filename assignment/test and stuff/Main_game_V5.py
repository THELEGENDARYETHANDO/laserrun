import pygame
import pygame.gfxdraw
import random
import fish_game
import time

#init pygame
pygame.init()
clock = pygame.time.Clock()

#colours
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
transparent_yellow = (255, 255, 0, 100)
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
title_img = pygame.image.load("assignment\pictures\Comp Sci game title screen.png")
background = pygame.image.load("assignment\pictures\Comp sci background.png")

font1 = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 100)

def text(text, font):
    text_surface = font.render(text, True, white)
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
    global playing, title, start_time, bomb_spawn_seconds, laser_spawn_time, laser, hori_laser, vert_laser
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
    laser_spawn_time = 0
    bomb_spawn_seconds = 0
    laser = Laser()
    hori_laser = Horizontal_Laser()
    vert_laser = Vertical_Laser()

def start_bomb_mayhem():
    global playing, title, start_time, bomb_spawn_seconds, bomb_mayhem
    playing = True
    title = False
    start_time = pygame.time.get_ticks()
    bomb_spawn_seconds = 0
    bomb_mayhem = True

def Back_to_title():
    global title, death
    title = True
    death = False

fishing = False

def start_fish():
    global title, fishing
    title = False
    fishing = True

def stop_fish():
    global title, fishing
    title = True
    fishing = False

#laser variables
laser_img_num = 0
laser_img_time = 0
laser_spawn_time = 0
class Laser:
    def __init__(self):
        super().__init__()
        self.img_time = 0
        self.img_num = 0
    
    def spawn(self, Time):
        for i in range(Time // 10000 + 1):
            horizontal_laser_coords = Horizontal_Laser.spawn(laser)
            hori_laser.array.append([horizontal_laser_coords, pygame.time.get_ticks()])
        for i in range(Time // 7000 + 1):
            vertical_laser_coords = Vertical_Laser.spawn(laser)
            vert_laser.array.append([vertical_laser_coords, pygame.time.get_ticks()])

    def animation(self, Time):
        print(self.img_num)
        if Time - self.img_time > 25:
            if self.img_num < 3:
                self.img_num += 1
            else:
                self.img_num = 0
            self.img_time = Time

class Horizontal_Laser(Laser):
    def __init__(self):
        super().__init__()
        self.array = []
        self.hit = False

    def attack(self):
        for laser in self.array:
            self.life = (pygame.time.get_ticks() - laser[1])
            if self.life < 1000:
                pygame.gfxdraw.box(surface, (0, laser[0], screen_width, 32), transparent_yellow)
            elif self.life < 3000:
                self.animation(play_time)
                self.img = pygame.image.load(f"assignment\pictures\hori_laser{self.img_num}.png")
                surface.blit(self.img, (0, laser[0]))
                if player_y < laser[0] + 32 and player_y + 32 > laser[0] and jump != True:
                    self.hit = True
            elif self.life >= 3000:
                self.array.remove(laser)

    def spawn(self):
        self.width = screen_width
        self.height = 32
        self.y_pos = random.randint(0, screen_height - 32)
        return (self.y_pos)

class Vertical_Laser(Laser):
    def __init__(self):
        super().__init__()
        self.array = []
        self.hit = False

    def attack(self):
        for laser in self.array:
            vertical_laser_life = (pygame.time.get_ticks() - laser[1])
            if vertical_laser_life < 1000:
                pygame.gfxdraw.box(surface, (laser[0], 0, 32, screen_height), transparent_yellow)
            elif vertical_laser_life < 3000: 
                self.animation(play_time)
                self.img = pygame.image.load(f"assignment\pictures/vert_laser{self.img_num}.png")
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
#Create instances of laser classes

#player variables
player_img = pygame.image.load("assignment/pictures/the guy.png")
player_x = 604
player_y = 400
player_speed = 8
start_time = 0
death_msg = "DEATH"
best_time = 0.0
bomb_mayhem_best_time = 0.0
play_time = 0
jump_time = 0

#bomb variables
bomb_spawn_seconds = 0
bomb_spawn_num = 0
bomb_spawn_time = 500
bomb_red = pygame.Color("#ae1b1b")
bomb_orange = pygame.Color("#db5a00")
bomb_yellow = pygame.Color("#ff9600")
bombs = []

title = True
playing = False
death = False
running = True
bomb_mayhem = False
fish_game.fishing = False
jump = False
#main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if title:
        bomb_mayhem = False
        screen.blit(surface, (0, 0))
        surface.blit(title_img, (0, 0))
        surface.blit(font1.render(f"Best time = {best_time/1000} seconds!", True, black), (screen_width - 300, screen_height - 20))
        surface.blit(font1.render(f"Bomb mayhem best time = {bomb_mayhem_best_time/1000} seconds!", True, black), (screen_width - 750, screen_height - 20))
        button("The Mystery Button", 500, 0, 240, 32, grey, light_grey, start_fish)
        button("START", screen_width - 272, screen_height - 102, 240, 70, grey, light_grey, start)
        button("Bomb Mayhem", screen_width - 512, screen_height - 102, 240, 70, grey, light_grey, start_bomb_mayhem)
        button("QUIT", 32, screen_height - 102, 240, 70, grey, light_grey, quit)
        pygame.display.update()

    if fishing:
        screen.blit(surface, (0, 0))
        keypress = pygame.key.get_pressed()
        surface.fill(blue)
        fish_game.fish()
        if keypress[pygame.K_f]:
            surface.blit(fish_game.fish_caught, (screen_width/2 - 32, screen_height/2 - 16))
        button("Stop fishing :(", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), stop_fish)
        pygame.display.update()

    if playing:
        rot_surface = pygame.transform.rotate(surface, surface_rotation)
        screen.blit(rot_surface, (0, 0))
        timer = pygame.time.get_ticks()
        play_time = timer - start_time
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
            player_img = pygame.image.load("assignment\pictures/the guy jump.png")
        if timer - jump_time > 500:
            jump = False
            player_img = pygame.image.load("assignment/pictures/the guy.png")
        surface.blit(player_img, (player_x, player_y))

        #Makes sure the lasers don't spawn if your playing bomb mayhem
        if bomb_mayhem != True:
            #Appends the coordinates of lasers that are spawning
            if play_time - laser_spawn_time > 3000:
                laser.spawn(play_time)
                laser_spawn_time = play_time

            #Spawns the lasers on the screen and determines if they are harmful or not
            hori_laser.attack()
            vert_laser.attack()

            if hori_laser.hit or vert_laser.hit:
                pygame.display.update()
                time.sleep(0.5)  # Introduce a delay if desired
                death_msg = "Death by laser"
                playing = False
                death = True

        #gets the coulour of the pixel at each corner of the player
        player_pixel_colour1 = screen.get_at((int(player_x), int(player_y)))
        player_pixel_colour2 = screen.get_at((int(player_x + 20), int(player_y)))
        player_pixel_colour3 = screen.get_at((int(player_x), int(player_y + 32)))
        player_pixel_colour4 = screen.get_at((int(player_x + 20), int(player_y + 32)))

        if bomb_mayhem == True:
            bomb_spawn_num = 1
        else:
            bomb_spawn_num = 2

        if bomb_mayhem == True:
            if bomb_spawn_time > 100:
                bomb_spawn_time = 600 - (play_time // 100)
            else:
                bomb_spawn_time = 100
        else:
            bomb_spawn_time = 2500

        if play_time - bomb_spawn_seconds > bomb_spawn_time:
            for i in range(bomb_spawn_num):
                bombs.append([random.randint(-112, screen_width - 144), random.randint(-112, screen_height - 144), 0, 0]) # makes sure the bombs always spawn on the screen
            bomb_spawn_seconds = play_time
        for bomb in bombs:
            if bomb[2] < 6:
                pygame.gfxdraw.filled_circle(surface, bomb[0] + 128, bomb[1] + 128, 150, transparent_yellow)
            bomb_pic = pygame.image.load(f"assignment/pictures/bomb{bomb[2]}.png")
            surface.blit(bomb_pic, (bomb[0], bomb[1]))
            if play_time - bomb[3] > 250:
                if bomb[2] < 9:
                    bomb[2] += 1
                    bomb[3] = play_time
                else:
                    bombs.remove(bomb)
            if bomb[2] >= 6:
                #detects if the colour at each corner of the player is one of the coulours used in the bomb explosion
                if player_pixel_colour1 == (bomb_yellow) or player_pixel_colour2 == (bomb_yellow) or player_pixel_colour3 == (bomb_yellow) or player_pixel_colour4 == (bomb_yellow) or player_pixel_colour1 == (bomb_orange) or player_pixel_colour2 == (bomb_orange) or player_pixel_colour3 == (bomb_orange) or player_pixel_colour4 == (bomb_orange) or player_pixel_colour1 == (bomb_red) or player_pixel_colour2 == (bomb_red) or player_pixel_colour3 == (bomb_red) or player_pixel_colour4 == (bomb_red):
                    pygame.display.update()
                    time.sleep(0.5)
                    death_msg = "Death by bomb"
                    death = True
                    playing = False
        try:
            if bombs[0][2] >= 6:
                surface_rotation = random.uniform(-0.5, 0.5)
        except:
            surface_rotation = 0
        surface.blit(font1.render(f"Time: {play_time/1000}", True, red), (0, screen_height - 60))
        #button("QUIT", 0, 0, 240, 70, (100, 100, 100), (200, 200, 200), quit)
        pygame.display.update()
        clock.tick(30)

    if death:
        vert_laser.hit = False
        hori_laser.hit = False
        if play_time > best_time and bomb_mayhem == False:
            best_time = play_time
        if play_time > bomb_mayhem_best_time and bomb_mayhem == True:
            bomb_mayhem_best_time = play_time
        bomb_spawn_time = 2500
        laser_img_time = 0
        screen.blit(surface, (0, 0))
        surface.fill(black)
        button("Back to Title", (screen_width - 240)/2, (screen_height - 70)/2, 240, 70, (100, 100, 100), (200, 200, 200), Back_to_title)
        surface.blit(font1.render(death_msg, True, red), (550, 100))
        surface.blit(font1.render(f"you survived for {play_time/1000} seconds", True, red), (450, 400))
        for bomb in bombs:
            bombs.remove(bomb)
        #for laser in hori_laser.array:
        #    hori_laser.array.remove(laser)
        #for laser in vert_laser.array:
        #    vert_laser.array.remove(laser)
        pygame.display.update()
print("end")
pygame.quit()