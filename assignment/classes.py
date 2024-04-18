import pygame
import pygame.gfxdraw
import math
import random

screen_height = 560
screen_width = 1240

class Laser:
    def __init__(self):
        self.img_time = 0
        self.img_num = 0

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
        self.hit = False
        self.spawn_time = 0
        self.array = []

    def spawn(self, time):
        if time - self.spawn_time > 3000:
            for i in range(time // 10000 + 1):
                self.array.append([random.randint(0, screen_height - 32), time, 0])
            self.spawn_time = time

    def attack(self, time, plane, colour, y, jump):
        ##attack(play_time, surface, transparent_yellow, player_y, jump)
        for laser in self.array:
            laser[2] = time - laser[1]
            if laser[2] < 1000:
                pygame.gfxdraw.box(plane, (0, laser[0], screen_width, 32), colour)
            elif laser[2] < 3000:
                self.animation(pygame.time.get_ticks())
                img = pygame.image.load(f"assignment/pictures/hori_laser{self.img_num}.png")
                plane.blit(img, (0, laser[0]))
                if y < laser[0] + 32 and y + 32 > laser[0] and jump != True:
                    self.hit = True
            else:
                self.array.remove(laser)
    
    def reset(self):
        for laser in self.array:
            self.array.remove(laser)
            self.hit = False
            self.img_time = 0

class Vertical_Laser(Laser):
    def __init__(self):
        super().__init__()
        self.hit = False
        self.array = []
        self.spawn_time = 0

    def spawn(self, time):
        if time - self.spawn_time > 3000:
            for i in range(time // 10000 + 1):
                self.array.append([random.randint(0, screen_width - 32), time, 0])
            self.spawn_time = time


    def attack(self, time, plane, colour, x, jump):
        ##attack(play_time, surface, transparent_yellow, player_x, jump)
        for laser in self.array:
            laser[2] = time - laser[1]
            if laser[2] < 1000:
                pygame.gfxdraw.box(plane, (laser[0], 0, 32, screen_height), colour)
            elif laser[2] < 3000: 
                self.animation(pygame.time.get_ticks())
                img = pygame.image.load(f"assignment/pictures/vert_laser{self.img_num}.png")
                plane.blit(img, (laser[0], 0))
                if x < laser[0] + 20 and x + 20 > laser[0] and jump != True:
                    self.hit = True
            else:
                self.array.remove(laser)
    
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

    def spawn(self, time, state):
        ##spawn(play_time, bomb_mayhem)
        #Determines how many bombs will spawn at a time
        if state == True:
            self.spawn_num = 1
        else:
            self.spawn_num = 2
        #determines the interval between bomb spawn times (caps out at 100 miliseconds in bomb mayhem)
        if state == True:
            self.spawn_time = 600 - (time // 100) 
            if self.spawn_time <= 100:
                self.spawn_time = 100
        else:
            self.spawn_time = 2500
        #Appends the bombs into an array to spawn them
        if time - self.last_spawn_time > self.spawn_time:
            for i in range(self.spawn_num):
                self.array.append([random.randint(-112, screen_width - 144), random.randint(-112, screen_height - 144), 0, 0, 128]) # makes sure the bombs always spawn on the screen
            self.last_spawn_time = time

    def attack(self, time, x, y, plane):
        ##(play_time, player_x, player_y, surface)
        for bomb in self.array:
            if bomb[2] == 6:
                bomb[4] = 32
            elif bomb[2] == 7:
                bomb[4] = 64
            elif bomb[2] == 8:
                bomb[4] = 96
            elif bomb[2] >= 9:
                bomb[4] = 128
            
            #manages the animation for the bomb: bomb[2] is the frame number and bomb[3] is the time since the last frame of the animation
            if time - bomb[3] > 250:
                if bomb[2] < 11:
                    bomb[2] += 1
                    bomb[3] = time
                else:
                    self.array.remove(bomb)
            bomb_pic = pygame.image.load(f"assignment/pictures/bomb{bomb[2]}.png")
            plane.blit(bomb_pic, (bomb[0], bomb[1]))

            circle_x = bomb[0] + 128 #gets the x coord in the middle of the bomb
            circle_y = bomb[1] + 128 #gets the y coord in the middle of the bomb
            circle_r = bomb[4] #bom[4] is the radius of the bomb explosion
            pygame.gfxdraw.filled_circle(plane, circle_x, circle_y, circle_r, (0, 0, 0, 0))

            #calculate the closest point on the players hitbox to the circle
            closest_x = max(x, min(circle_x, x + 20))
            closest_y = max(y, min(circle_y, y + 32))
            #calculate the distance between the circle's center and the closest point on the players hitbox
            distance = math.sqrt((circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2)
            #check if the distance is less than the circle's radius
            if distance < circle_r and bomb[2] > 6:
                self.hit = True

    def reset(self):
        for bomb in self.array:
            self.array.remove(bomb)
            self.hit = False
            self.last_spawn_time = 0