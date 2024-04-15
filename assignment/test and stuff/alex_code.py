# importing pygame module and others
import pygame, pygame.freetype
import random
import time
import math
from collections import deque

# importing sys module
import sys

# initialising pygame
pygame.init()

# creating display
gamesize = [800,800]
display = pygame.display.set_mode((gamesize[0],gamesize[1]))
windowsize = display.get_size()

maxfps = 60 # The natural capped FPS of the game.
gamespeed = 1

clock = pygame.time.Clock()

occupied_tiles = []
collidableobj = []
bulletcollidable = []
team1,team1rects = [],[]
team2,team2rects = [],[]

debugai = False

# Defines the values of the nav mesh generation
maptilesize = 50
mapwidth = 60
mapheight = 60
mapstart = [0,0]

#If true, all objects in the game except the menu will be paused
GamePaused = False

#Defines the values of the total offset since the player moves. This might've gone unused since there will be a health system instead of respawns
totaloffset = [0,0]

def getdistanceto(startpos,targetpos): #Gets the distance from two points by finding the hypotenuse via pythagoras
    plrpos = [targetpos[0],targetpos[1]]
    mypos = [startpos[0],startpos[1]]
    offset = [mypos[0]-plrpos[0],mypos[1]-plrpos[1]]
    if offset[0] <= 0: offset[0] *= -1
    if offset[1] <= 0: offset[1] *= -1
    num1 = offset[0]**2
    num2 = offset[1]**2
    return math.sqrt(num1+num2)

def getangleto(pos1, pos2):
    return (math.atan2(pos2[0]-pos1[0],pos2[1]-pos1[1]) * 180 / math.pi)

def createrect(point1x, point1y, point2x, point2y): #Draws a rectangle between two points and returns it. Makes it easier for me to create the levels and rooms
    return pygame.rect.Rect((point1x, point1y, point2x-point1x, point2y-point1y))

def renderrect(self,surface,color): #Draw a rectangle to the screen
    pygame.draw.rect(surface, color, self)
def renderimg(self,surface,pos,size): #Blit an image to the screen
    surface.blit(self,[pos[0]-size[0]/2,pos[1]-size[1]/2])

def blitRotateCenter(surf, image, topleft, angle): #Rotate an image and blit it to the display
    rotated_image = pygame.transform.rotate(image, angle[0]) #transform the image
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center) #Create the new position of the image

    surf.blit(rotated_image, new_rect) # Blit it to the screen

def checklos(pos1 : list,pos2 : list,maxdepth : int,sightboxsize : int): # check if there is a line of sight between two points
    if not sightboxsize:
        sightboxsize = 1
    angle = getangleto(pos1,pos2)
    dist = getdistanceto(pos1,pos2)
    stepspeed = calculate_movement(dist/maxdepth,math.radians(angle))
    for depth in range(maxdepth):
        testrect = createrect(pos1[0]-sightboxsize/2,pos1[1]-sightboxsize/2,pos1[0]+sightboxsize/2,pos1[1]+sightboxsize/2)
        testrect.move_ip(stepspeed[0]*depth,stepspeed[1]*depth)
        if debugai:
            pygame.draw.rect(display, (255,0,0), testrect)
        collisions = pygame.Rect.collidelist(testrect,collidableobj)
        if collisions != -1:
            if not collidableobj[collisions] in team2:
                return False
    return True

class gameobject(object):
    def __init__(self,name : str,visible : bool,size : list,position : list,hascolisions : bool,image : str,colour : tuple,transparency : float,rotation : int,customclass,StaticObject : bool, screenlayer : int):
        self.name = name or "NoName"
        self.visible = visible or False
        self.size = size or None
        self.position = position.copy() or None
        if size and position:
            self.rect = createrect(totaloffset[0] + self.position[0]-self.size[0]/2,totaloffset[1] + self.position[1]-self.size[1]/2, totaloffset[0] + self.position[0]+self.size[0]/2,totaloffset[1] + self.position[1]+self.size[1]/2)
        else:
            self.rect = None
        self.image = image or None
        self.hascolisions = hascolisions or False
        self.colour = colour or [128,0,128]
        self.transparency = transparency or 0
        self.rotation = rotation or 0
        self.customclass = customclass or None
        self.StaticObject = StaticObject or False
        self.screenlayer = screenlayer or 0

    def update(self):
        if self.position and self.rect and not self.StaticObject:
            try:
                self.rect.center = self.position
            except:
                print("Failed to Update Object Position:",self.name)
        if self.customclass:
            #try:
                returnvalue = self.customclass.update(myobject)
                if returnvalue == "deleteme":
                    objects.remove(self)
            #except Exception as error:
                #print("Failed to Update Custom Class:",self.name," Error:",error)

    def __lt__(self, other):
         return self.screenlayer < other.screenlayer

class text(object):
    def __init__(self,name : str,text : str,font,fontsize : float,textcolour : tuple):
        self.name = name or "Text"
        self.text = text or "NOTEXT"
        self.fontsize = fontsize or 16
        self.textcolour = textcolour or (0,0,0)
        self.font = font or "arial"
        self.finalfont = pygame.freetype.SysFont(self.font,self.fontsize)

    def update(self,myobject):
        self.finalfont = pygame.freetype.SysFont(self.font,self.fontsize)
        return

class particle(object):
    def __init__(self,name : str,velocityrange : list,lifetime : float,anglerange : list):
        self.name = name or "Particle"
        self.velocityrange = velocityrange or [0,0]
        self.anglerange = anglerange or [0,0]
        self.lifetime = lifetime or 1
        self.maxlifetime = self.lifetime

        self.angle = random.randint(self.anglerange[0],self.anglerange[1])
        self.velocity = calculate_movement(random.randint(self.velocityrange[0],self.velocityrange[1]),math.radians(self.angle))

    def update(self,myobject):
        if self.velocity and myobject:
            myobject.position[0] += self.velocity[0]
            myobject.position[1] += self.velocity[1]
            self.lifetime -= (deltaseconds*gamespeed)
            myobject.transparency = self.lifetime/self.maxlifetime
            if self.lifetime <= 0:
                return "deleteme"
        else:
            return "deleteme"

class firefly(object):
    def __init__(self,name : str,speed: int):
        self.name = name or "Firefly"
        self.speed = speed or 1
        self.mydir = random.randint(0,1)
        self.angle = 0

    def update(self,myobject):
        if self.speed and myobject:
            randomint = random.randint(-5,5)
            if randomint == -5 and self.mydir == 1:
                self.mydir = 0
            elif randomint == 5 and self.mydir == 0:
                self.mydir = 1
            if self.mydir == 1:
                self.angle += 5
            elif self.mydir == 0:
                self.angle -= 5
            if self.angle >= 360:
                self.angle -= 360
            if self.angle < 0:
                self.angle += 360
            newx,newy = calculate_movement(self.speed,math.radians(self.angle))
            myobject.position[0] += newx*(deltaseconds*gamespeed)
            myobject.position[1] += newy*(deltaseconds*gamespeed)
        else:
            return "deleteme"

class temporary(object):
    def __init__(self,name : str,lifetime: float):
        self.name = name or "TemporaryObj"
        self.lifetime = lifetime or 1
        self.totallifetime = self.lifetime

    def update(self,myobject):
        if myobject:
            self.lifetime -= (deltaseconds*gamespeed)
            if self.lifetime <= 0:
                return "deleteme"
        else:
            return "deleteme"

class bullet(object):
    def __init__(self,name : str,velocity : list, lifetime : float, team : int):
        self.name = name or "BulletSubClass"
        self.velocity = velocity or None
        self.lifetime = lifetime or 10
        self.team = team

    def deletionparticles(self,myobject):
        for x in range(3):
            objects.append(gameobject("Particle",True,[random.randint(3,5),random.randint(3,5)],list(myobject.rect.center),False,None,(255,255,0),0,None,particle("Bullet",[-10,10],0.2,[0,360]),False,4))

    def update(self,myobject):
        if self.velocity and myobject:
            myobject.position[0] += self.velocity[0]
            myobject.position[1] += self.velocity[1]
            collidelist = pygame.Rect.collidelist(myobject.rect,bulletcollidable)
            collideobj = bulletcollidable[collidelist]
            if collidelist != -1 and collideobj not in team1 and collideobj not in team2:
                """mask = pygame.mask.Mask((collideobj.width, collideobj.height))
                mask.fill()
                other = pygame.mask.Mask((myobject.rect.width, myobject.rect.height))
                other.fill()
                dx = mask.overlap_area(other, (myobject.rect.x-collideobj.x + 1, myobject.rect.y-collideobj.y)) - mask.overlap_area(other, (myobject.rect.x-collideobj.x - 1, myobject.rect.y-collideobj.y))
                dy = mask.overlap_area(other, (myobject.rect.x-collideobj.x, myobject.rect.y-collideobj.y + 1)) - mask.overlap_area(other, (myobject.rect.x-collideobj.x, myobject.rect.y-collideobj.y - 1))"""

                self.deletionparticles(myobject)
                return "deleteme"
            if self.team == 1:
                enemies = pygame.Rect.collidelist(myobject.rect,team2rects)
                if enemies != -1:
                    collideobj = team2[enemies]
                    self.deletionparticles(myobject)
                    return "deleteme"
            if self.team == 2:
                enemies = pygame.Rect.collidelist(myobject.rect,team1rects)
                if enemies != -1:
                    collideobj = team1[enemies]
                    self.deletionparticles(myobject)
                    return "deleteme"
            self.lifetime -= (deltaseconds*gamespeed)
            if self.lifetime <= 0:
                self.deletionparticles(myobject)
                return "deleteme"
        else:
            return "deleteme"

class Weapon(object):
    def __init__(self, damage : int, bulletsize : int, bulletspeed : float, bulletspershot : int, accuracy : float, anglespread, bpm : float, bulletcolour : tuple, bulletlife : float, team : int):
        self.damage = damage or 0
        self.bulletspershot = bulletspershot or 1
        self.accuracy = accuracy or 1
        self.anglespread = anglespread or 0
        self.bulletsize = bulletsize or 5
        self.bulletvelocity = bulletspeed or 15
        self.firedelay = 60/bpm or .5
        self.firedb = 0
        self.bulletcolour = bulletcolour or (255,255,0)
        self.team = team or 1
        self.bulletlifetime = bulletlife or 5

    def fire(self,frompos):
        if self.firedb <= 0:
            if isinstance(frompos,tuple): frompos = list(frompos)
            self.firedb = self.firedelay
            mousepos = pygame.mouse.get_pos()
            angle = getangleto(frompos,list(mousepos))
            for n in range(self.bulletspershot):
                deviation = (int(self.bulletspershot/2)-self.bulletspershot + n+1) * (self.anglespread/int(self.bulletspershot/2 + 0.5))
                objects.append(gameobject("bullet",True,[self.bulletsize,self.bulletsize],frompos,False,None,self.bulletcolour,0,0,bullet(None,calculate_movement(self.bulletvelocity,math.radians(angle+deviation)),self.bulletlifetime,self.team),False,3))

    def update(self):
        if self.firedb > 0:
            self.firedb -= ((deltaseconds*gamespeed))

class EnemyAI(object):
    def __init__(self,AIType : int,myenemy,myobject,weapon):
        self.myai = AIType
        self.myenemy = myenemy
        self.myobject = myobject
        self.weapon = weapon

    def update(self):
        if self.myai == 1 and self.myenemy and self.myobject:
            tilexpos = round((self.myenemy.target.rect.centerx - objects[0].rect.centerx) / maptilesize,0)
            tileypos = round((self.myenemy.target.rect.centery - objects[0].rect.centery) / maptilesize,0)

            mytilexpos = round((self.myobject.rect.centerx - objects[0].rect.centerx) / maptilesize,0)
            mytileypos = round((self.myobject.rect.centery - objects[0].rect.centery) / maptilesize,0)

            self.myenemy.myxpos = mytilexpos
            self.myenemy.myypos = mytileypos

            if (tilexpos,tileypos) in occupied_tiles:
                self.myenemy.moving = False
                return

            self.myenemy.moving = True
            if self.myenemy.haslos:
                angle = getangleto(myobject.position,list(self.myenemy.target.rect.center))
                movement = calculate_movement(self.myenemy.speed,math.radians(angle))
                self.myenemy.velocity[0] += movement[0] * (deltaseconds*gamespeed)
                self.myenemy.velocity[1] += movement[1] * (deltaseconds*gamespeed)
                self.weapon.fire(myobject.position)
            else:
                next_pos,path = pathfinding.get_path((mytilexpos,mytileypos), (tilexpos,tileypos))
                next_x, next_y = next_pos

                maproot = objects[0].rect
                if debugai:
                    for next in path:
                        newx,newy = next
                        objects.append(gameobject(None,True,[20,20],[maproot.centerx+newx * maptilesize, maproot.centery+newy * maptilesize],False,None,(0,255,0),0,0,particle("Path",[0,0],0.3,[0,0]),False,1))
                if next_pos and next_pos not in occupied_tiles:
                    if self.myenemy.targetdist < maptilesize*0.8:
                        angle = getangleto(self.myobject.position,list(self.myenemy.target.rect.center))
                        movement = calculate_movement(self.myenemy.speed,math.radians(angle))
                        self.myenemy.velocity[0] += movement[0] * (deltaseconds*gamespeed)
                        self.myenemy.velocity[1] += movement[1] * (deltaseconds*gamespeed)
                    else:
                        angle = getangleto(self.myobject.position,[maproot.centerx+next_x*maptilesize,maproot.centery+next_y*maptilesize])
                        movement = calculate_movement(self.myenemy.speed,math.radians(angle))
                        self.myenemy.velocity[0] += movement[0] * (deltaseconds*gamespeed)
                        self.myenemy.velocity[1] += movement[1] * (deltaseconds*gamespeed)

class EntityCollisions(object):
    def __init__(self,collisiontype : int,myentity,myobject):
        self.mycollisiontype = collisiontype
        self.myentity = myentity
        self.myobject = myobject

    def update(self):
        if self.mycollisiontype == 0:
            hitting,timeout = True,30
            mypos = self.myobject.position
            while hitting: #Collision detection, creates a bunch of ghost squares which detect whether the player can move in that direction or not and slows them down until they aren't colliding, this will cause the game to crash if there is an event when the player is inside of a collision box
                myvel = self.myentity.velocity.copy()
                if myvel[0] < 0:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) + 0.5)
                if myvel[1] < 0:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) + 0.5)
                testhit = self.myobject.rect.copy()
                testhit.center = (mypos[0]+myvel[0],mypos[1])
                pygame.draw.rect(display,(255,0,0),testhit)
                hitx = False
                test = pygame.Rect.collidelist(testhit,collidableobj)
                if test != -1:
                    if collidableobj[test] != self.myobject and collidableobj[test] not in team2rects:
                        hitx = True
                if hitx:
                    if self.myentity.velocity[0] < 0:
                        self.myentity.velocity[0] += 1
                    if self.myentity.velocity[0] > 0:
                        self.myentity.velocity[0] -= 1

                if not hitx:
                    hitting = False
                else:
                    if abs(self.myentity.velocity[0]) < 1:
                        self.myentity.velocity[0] = 0
                    timeout -= 1
                    if timeout <= 1:
                        hitting = False
                        print("Object Collision Detection too Deep:",self.myobject.name)
            hitting,timeout = True,30
            mypos = self.myobject.position
            while hitting: #Collision detection, creates a bunch of ghost squares which detect whether the player can move in that direction or not and slows them down until they aren't colliding, this will cause the game to crash if there is an event when the player is inside of a collision box
                myvel = self.myentity.velocity.copy()
                if myvel[0] < 0:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) + 0.5)
                if myvel[1] < 0:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) + 0.5)
                testhit = self.myobject.rect.copy()
                testhit.center = (mypos[0]+myvel[0],mypos[1]+myvel[1])
                hity = False
                test = pygame.Rect.collidelist(testhit,collidableobj)
                if test != -1:
                    if collidableobj[test] != self.myobject and collidableobj[test] not in team2rects:
                        hity = True
                if hity:
                    if self.myentity.velocity[1] < 0:
                        self.myentity.velocity[1] += 1
                    if self.myentity.velocity[1] > 0:
                        self.myentity.velocity[1] -= 1

                if not hity:
                    hitting = False
                else:
                    if abs(self.myentity.velocity[1]) < 1:
                        self.myentity.velocity[1] = 0
                    timeout -= 1
                    if timeout <= 1:
                        hitting = False
                        print("Object Collision Detection too Deep:",self.myobject.name)
        elif self.mycollisiontype == 1:
            hitting,timeout = True,30
            mypos = self.myobject.position
            while hitting: #Collision detection, creates a bunch of ghost squares which detect whether the player can move in that direction or not and slows them down until they aren't colliding, this will cause the game to crash if there is an event when the player is inside of a collision box
                myvel = self.myentity.velocity.copy()
                if myvel[0] < 0:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) + 0.5)
                if myvel[1] < 0:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) + 0.5)
                testhit = self.myobject.rect.copy()
                testhit.center = (mypos[0]+myvel[0],mypos[1])
                hitx = False
                test = pygame.Rect.collidelist(testhit,collidableobj)
                if test != -1:
                    if collidableobj[test] != self.myobject:
                        hitx = True
                if hitx:
                    if self.myentity.velocity[0] < 0:
                        self.myentity.velocity[0] += 1
                    if self.myentity.velocity[0] > 0:
                        self.myentity.velocity[0] -= 1

                if not hitx:
                    hitting = False
                else:
                    if abs(self.myentity.velocity[0]) < 1:
                        self.myentity.velocity[0] = 0
                    timeout -= 1
                    if timeout <= 1:
                        hitting = False
                        print("Object Collision Detection too Deep:",self.myobject.name)
            hitting,timeout = True,30
            mypos = self.myobject.position
            while hitting: #Collision detection, creates a bunch of ghost squares which detect whether the player can move in that direction or not and slows them down until they aren't colliding, this will cause the game to crash if there is an event when the player is inside of a collision box
                myvel = self.myentity.velocity.copy()
                if myvel[0] < 0:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[0] = round(myvel[0] * ((deltaseconds*gamespeed)*100) + 0.5)
                if myvel[1] < 0:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) - 0.5)
                else:
                    myvel[1] = round(myvel[1] * ((deltaseconds*gamespeed)*100) + 0.5)
                testhit = self.myobject.rect.copy()
                testhit.center = (mypos[0]+myvel[0],mypos[1]+myvel[1])
                hity = False
                test = pygame.Rect.collidelist(testhit,collidableobj)
                if test != -1:
                    if collidableobj[test] != self.myobject:
                        hity = True
                if hity:
                    if self.myentity.velocity[1] < 0:
                        self.myentity.velocity[1] += 1
                    if self.myentity.velocity[1] > 0:
                        self.myentity.velocity[1] -= 1

                if not hity:
                    hitting = False
                else:
                    if abs(self.myentity.velocity[1]) < 1:
                        self.myentity.velocity[1] = 0
                    timeout -= 1
                    if timeout <= 1:
                        hitting = False
                        print("Object Collision Detection too Deep:",self.myobject.name)
            self.myobject.position[0] += self.myentity.velocity[0]
            self.myobject.position[1] += self.myentity.velocity[1]
            afterhit = self.myobject.rect.copy()
            afterhit.center = afterhit.center
            test = pygame.Rect.collidelist(afterhit,collidableobj)
            if test != -1:
                if collidableobj[test] != self.myobject:
                    self.myobject.position[0] -= self.myentity.velocity[0]
                    self.myobject.position[1] -= self.myentity.velocity[1]
            if self.myentity.velocity[0] > 0 and not self.myentity.moving:
                self.myentity.velocity[0] -= self.myentity.speed*(deltaseconds*gamespeed) * 0.8
            if abs(self.myentity.velocity[0]) < self.myentity.speed*(deltaseconds*gamespeed) * 0.8:
                self.myentity.velocity[0] = 0
            if self.myentity.velocity[0] < 0 and not self.myentity.moving:
                self.myentity.velocity[0] += self.myentity.speed*(deltaseconds*gamespeed) * 0.8
                if abs(self.myentity.velocity[0]) < self.myentity.speed*(deltaseconds*gamespeed) * 0.8:
                    self.myentity.velocity[0] = 0
            if self.myentity.velocity[1] > 0 and not self.myentity.moving:
                self.myentity.velocity[1] -= self.myentity.speed*(deltaseconds*gamespeed) * 0.8
                if abs(self.myentity.velocity[1]) < self.myentity.speed*(deltaseconds*gamespeed) * 0.8:
                    self.myentity.velocity[1] = 0
            if self.myentity.velocity[1] < 0 and not self.myentity.moving:
                self.myentity.velocity[1] += self.myentity.speed*(deltaseconds*gamespeed) * 0.8
                if abs(self.myentity.velocity[1]) < self.myentity.speed*(deltaseconds*gamespeed) * 0.8:
                    self.myentity.velocity[1] = 0
            if self.myentity.velocity[0] > self.myentity.speedcap:
                self.myentity.velocity[0] -= self.myentity.speed*(deltaseconds*gamespeed) * 3
            if self.myentity.velocity[0] < -self.myentity.speedcap:
                self.myentity.velocity[0] -= -self.myentity.speed*(deltaseconds*gamespeed) * 3
            if self.myentity.velocity[1] > self.myentity.speedcap:
                self.myentity.velocity[1] -= self.myentity.speed*(deltaseconds*gamespeed) * 3
            if self.myentity.velocity[1] < -self.myentity.speedcap:
                self.myentity.velocity[1] -= -self.myentity.speed*(deltaseconds*gamespeed) * 3

class enemy(object):
    def __init__(self,name : str,speed : int,speedcap : int,maxhp : int,enemytype : str, aggro : bool, mygun : Weapon):
        self.name = name or "BulletSubClass"
        self.speed = speed or None
        self.speedcap = speedcap or 999
        self.maxhp = maxhp
        self.hp = maxhp
        self.enemytype = enemytype
        self.velocity = [0,0]
        self.target = None
        self.ai = None
        self.collisions = None
        self.myxpos = 0
        self.myypos = 0
        self.aggro = aggro or False
        self.haslos = False
        self.target = None
        self.targetdist = 999
        self.retarget = .5
        self.maxdist = maptilesize * 50
        self.weapon = mygun or Weapon(1,5,15,1,1,0,120,None,2)
        self.moving = False

    def update(self,myobject):
        self.retarget -= (deltaseconds*gamespeed)
        self.myobject = myobject
        if not self.ai:
            self.ai = EnemyAI(1,self,myobject,self.weapon)
        if not self.collisions:
            self.collisions = EntityCollisions(1,self,myobject)
        if self.speed and self.myobject and self.weapon:

            if self.retarget <= 0:
                closesttarget,targetdist = None,99999

                for object in objects:
                    if isinstance(object.customclass,Player):
                        dist = getdistanceto(self.myobject.position,list(object.rect.center))
                        if targetdist > dist and dist < self.maxdist:
                            if not self.aggro:
                                haslineofsight = checklos(self.myobject.position,list(object.rect.center),round(dist/(maptilesize*0.7))+1,self.myobject.rect.width)
                                if haslineofsight:
                                    self.aggro = True
                                    closesttarget = object
                                    targetdist = dist
                            else:
                                closesttarget = object
                                targetdist = dist

                if closesttarget:
                    self.target = closesttarget
                    self.targetdist = targetdist
                    self.haslos = checklos(self.myobject.position,list(object.rect.center),round(dist/(maptilesize*0.7))+1,self.myobject.rect.width)

                self.retarget = .5

            if self.target in objects:
                self.ai.update()
                self.collisions.update()
        else:
            return "deleteme"

class Player(object):
    def __init__(self,name : str, maxhp : int, maxspeed : int):
        self.name = name or "PLAYER"
        self.dead = False
        self.pausemovement = False
        self.hp = maxhp or 5
        self.maxhp = maxhp or 5
        self.dashing = 0
        self.dashdb = 0
        self.damagedb = 0
        self.speedcap = maxspeed or 25
        self.shakeoffset = [0,0]
        self.collisions = None
        self.velocity = [0,0]
        self.speed = self.speedcap*5

    def damage(self): # when a player is damaged the get a damage cooldown so they are invulnerable during this time. If they run out of hp they die and respawn
        if self.damagedb > 0: return
        self.hp -= 1
        xshake = random.randint(1,2)
        if xshake == 1:
            xshake = 15
        else:
            xshake = -15
        yshake = random.randint(1,2)
        if yshake == 1:
            yshake = 15
        else:
            yshake = -15
        self.shakeoffset = [xshake,xshake]
        moveobjects(self.shakeoffset[0],self.shakeoffset[1])
        self.damagedb = 1
        self.colour = (255,0,0)
        if self.hp <= 0:
            self.dead = True
            self.colour = (255,0,0)
            self.rect.centery = 900
            self.hp = 1

    def update(self, myobject):
        if not self.collisions:
            self.collisions = EntityCollisions(0,self,myobject)
        if self.dashdb > 0:
            self.dashdb -= ((deltaseconds*gamespeed))
        if self.dashdb <= 0:
            self.dashdb = 0
            self.colour = (0, 162, 255)
        if self.shakeoffset[0] != 0 or self.shakeoffset[1] != 0:
            if self.shakeoffset[0] > 0:
                self.shakeoffset[0] -= 1
                moveobjects(-1,0)
            elif self.shakeoffset[0] < 0:
                self.shakeoffset[0] += 1
                moveobjects(1,0)
            if self.shakeoffset[1] > 0:
                self.shakeoffset[1] -= 1
                moveobjects(0,-1)
            elif self.shakeoffset[1] < 0:
                self.shakeoffset[1] += 1
                moveobjects(0,1)
        if self.dead or self.pausemovement or GamePaused: return #If the player is dead or movement is paused, return nothing to stop movement
        key = pygame.key.get_pressed()
        global debugai
        if key[pygame.K_u]:
            debugai = False
        if key[pygame.K_y]:
            debugai = True

        if key[pygame.K_a]: #Movement Keys add velocity to the xvel and yvel
            if key[pygame.K_w]:
                self.velocity[0] -= self.speed*(deltaseconds*gamespeed)/2
                self.velocity[1] -= self.speed*(deltaseconds*gamespeed)/2
            elif key[pygame.K_s]:
                self.velocity[0] -= self.speed*(deltaseconds*gamespeed)/2
                self.velocity[1] += self.speed*(deltaseconds*gamespeed)/2
            else:
                self.velocity[0] -= self.speed*(deltaseconds*gamespeed)
        elif key[pygame.K_d]:
            if key[pygame.K_w]:
                self.velocity[0] += self.speed*(deltaseconds*gamespeed)/2
                self.velocity[1] -= self.speed*(deltaseconds*gamespeed)/2
            elif key[pygame.K_s]:
                self.velocity[0] += self.speed*(deltaseconds*gamespeed)/2
                self.velocity[1] += self.speed*(deltaseconds*gamespeed)/2
            else:
                self.velocity[0] += self.speed*(deltaseconds*gamespeed)
        else:
            if key[pygame.K_w]:
                self.velocity[1] -= self.speed*(deltaseconds*gamespeed)
            if key[pygame.K_s]:
                self.velocity[1] += self.speed*(deltaseconds*gamespeed)
        if self.velocity[0] > 0 and not key[pygame.K_d]:
            self.velocity[0] -= self.speed*(deltaseconds*gamespeed) * 0.8
            if abs(self.velocity[0]) < self.speed*(deltaseconds*gamespeed) * 0.8:
                self.velocity[0] = 0
        if self.velocity[0] < 0 and not key[pygame.K_a]:
            self.velocity[0] += self.speed*(deltaseconds*gamespeed) * 0.8
            if abs(self.velocity[0]) < self.speed*(deltaseconds*gamespeed) * 0.8:
                self.velocity[0] = 0
        if self.velocity[1] > 0 and not key[pygame.K_s]:
            self.velocity[1] -= self.speed*(deltaseconds*gamespeed) * 0.8
            if abs(self.velocity[1]) < self.speed*(deltaseconds*gamespeed) * 0.8:
                self.velocity[1] = 0
        if self.velocity[1] < 0 and not key[pygame.K_w]:
            self.velocity[1] += self.speed*(deltaseconds*gamespeed) * 0.8
            if abs(self.velocity[1]) < self.speed*(deltaseconds*gamespeed) * 0.8:
                self.velocity[1] = 0
        if self.velocity[0] > self.speedcap:
            self.velocity[0] -= self.speed*(deltaseconds*gamespeed) * 3
        if self.velocity[0] < -self.speedcap:
            self.velocity[0] -= -self.speed*(deltaseconds*gamespeed) * 3
        if self.velocity[1] > self.speedcap:
            self.velocity[1] -= self.speed*(deltaseconds*gamespeed) * 3
        if self.velocity[1] < -self.speedcap:
            self.velocity[1] -= -self.speed*(deltaseconds*gamespeed) * 3
        if key[pygame.K_SPACE]: # Dashing, sets the velocity to 20 in the direction the character is moving
            if self.dashdb <= 0 and (self.velocity[0]+self.velocity[1] != 0):
                self.dashdb = .5
                self.dashing = 1
                self.colour = (255,0,0)
                if key[pygame.K_d]:
                    self.velocity[0] = 15
                if key[pygame.K_a]:
                    self.velocity[0] = -15
                if key[pygame.K_w]:
                    self.velocity[1] = -15
                if key[pygame.K_s]:
                    self.velocity[1] = 15
        self.collisions.update()
        totaloffset[0] -= self.velocity[0] * ((deltaseconds*gamespeed)*100) #Move the total offset values
        totaloffset[1] -= self.velocity[1] * ((deltaseconds*gamespeed)*100)
        for myobject in objects: #Moves all of the objects in the game so that the player is centered
            if myobject.position and myobject.rect and not myobject.StaticObject:
                try:
                    myobject.position[0] -= self.velocity[0] * ((deltaseconds*gamespeed)*100)
                    myobject.position[1] -= self.velocity[1] * ((deltaseconds*gamespeed)*100)
                except:
                    print("Failed to Move Object:",myobject.name)

def generatemap(tilesize,tilesx,tilesy,topleft):
    mymap = []
    solidobj = []
    for myobject in objects:
        if myobject.hascolisions and not isinstance(myobject.customclass,Player) and not isinstance(myobject.customclass,enemy):
            solidobj.append(myobject.rect)
    for n in range(tilesy):
        row = []
        for i in range(tilesx):
            testrect = createrect(topleft[0]+i*tilesize+(tilesize/2-1),topleft[1]+n*tilesize+(tilesize/2-1),topleft[0]+i*tilesize+(tilesize/2+1),topleft[1]+n*tilesize+(tilesize/2+1))
            isoccupied = testrect.collidelist(solidobj)
            if isoccupied != -1:
                row.append(1)
                if debugai:
                    objects.append(gameobject("navmesh",True,[maptilesize-2,maptilesize-2],list(testrect.center),False,None,(255,0,0),0,0,temporary(None,1),False,1))
            else:
                row.append(False)
                #objects.append(gameobject("navmesh",True,[98,98],[topleft[0]+i*tilesize+tilesize/2,topleft[1]+n*tilesize+tilesize/2],False,None,(100,100,100),0,0,particle(None,None,1,None),False,1))
        mymap.append(row)
    return mymap

def generateworldmap(mini_map):
    worldmap = {}
    for j, row in enumerate(mini_map):
        for i, value in enumerate(row):
            if value:
                worldmap[(i, j)] = value
    return worldmap

class PathFinding:
    def __init__(self, mymap):
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.update(mymap)

    def update(self,mymap):
        self.map = mymap
        self.graph = {}
        self.world_map = generateworldmap(mymap)
        self.get_graph()

    def get_path(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1],path

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            try:
                next_nodes = graph[cur_node]
            except Exception as myerror:
                continue
                #print(myerror)

            try:
                for next_node in next_nodes:
                    if next_node not in visited and next_node not in occupied_tiles:
                        queue.append(next_node)
                        visited[next_node] = cur_node
            except Exception as myerror:
                print(myerror)
        return visited

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.world_map]

    def get_graph(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

#create function to manage text objects
def text_objects(text, font, colour):
    text_surface,text_rect = font.render(text, colour)
    return text_surface,text_rect

#menu button
def button(msg, x, y, w, h, inactive_colour, active_colour, action=None):
    #Get active mouse position on menu
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    #check to see if the mouse is hovering over the buttons
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(display, active_colour, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(display, inactive_colour, (x, y, w, h))

    #Text in the button
    small_text = pygame.font.SysFont('arial', 20)
    #Uses the text_objects function to return the value of the rectangle and the rendered text which fits in the rect
    text_surf, text_rect = text_objects(msg, small_text)
    #Position of the text in the button x+half the width of the button
    text_rect.center = ((x+(w/2)), (y+(h/2)))
    #put the button on screen
    display.blit(text_surf, text_rect)

def quit_game():
    pygame.quit()
    quit()

objects = [ # Objects table, all objects are put here as object classes INCLUDING the player
    gameobject("player",True,[16,16],[windowsize[0]/2,windowsize[1]/2],False,None,(0,162,255),None,0,Player("Player",5,4),True,999),
    # gameobject("rect",True,[200,1500],[100,750],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[500,100],[450,650],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[500,100],[550,850],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[100,300],[250,1150],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[100,500],[450,1150],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[100,500],[850,1050],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[100,300],[650,1150],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[1100,100],[850,1550],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[200,100],[700,1450],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[1000,100],[1000,1750],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[100,300],[150,1750],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[200,100],[300,1750],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[100,300],[150,2150],True,None,(255,255,255),None,0,None,False,1),
    # gameobject("rect",True,[100,200],[400,100],True,None,(255,255,255),None,45,None,False,1),
    gameobject("rect",True,[100,5],[100,250],True,None,(255,255,255),None,45,None,False,1),
    gameobject("firefly",True,[5,5],[0,0],False,None,(255,0,255),0.5,0,firefly(None,1),False,2),
    gameobject("enemy",True,[16,16],[450,2050],False,None,(255,0,255),0,0,enemy(None,10,4,10,1,False,Weapon(1,5,15,1,1,0,120,None,4,2)),False,3),
    gameobject("enemy",True,[16,16],[450,2250],False,None,(255,0,255),0,0,enemy(None,10,4,10,1,False,Weapon(1,5,15,1,1,0,120,None,4,2)),False,3),
    gameobject("enemy",True,[16,16],[450,2450],False,None,(255,0,255),0,0,enemy(None,10,4,10,1,False,Weapon(1,5,15,1,1,0,120,None,4,2)),False,3),
    gameobject("fps",True,[100,100],[150,150],False,None,(150,150,150),0,0,text(None,"FPS",None,40,(0,0,0)),True,3),
]

_ = None

objectmap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,_,1,_,_,_,_,_,1,_,_,1,_,_,1,1,1,1,1,_,1,_,_,_,_,_,_,_,_,1],
    [1,_,1,1,1,_,1,1,1,1,_,1,1,_,1,_,1,_,_,_,1,_,1,_,1,_,_,1,_,1],
    [1,_,1,_,1,_,_,1,_,1,_,_,_,_,1,_,_,_,1,_,_,_,_,_,1,_,_,_,_,1],
    [1,_,_,_,_,_,1,1,_,1,_,1,_,1,1,_,1,_,1,1,_,1,1,1,1,_,1,1,1,1],
    [1,1,1,_,1,_,1,_,_,_,_,1,_,_,_,_,1,_,1,_,_,1,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,1,_,_,1,1,_,1,_,1,_,_,_,1,1,_,1,_,_,_,1,_,1],
    [1,_,1,1,1,_,1,_,1,_,1,1,1,_,1,_,1,_,1,1,1,1,_,1,1,1,_,_,_,1],
    [1,_,1,1,_,_,1,1,1,_,1,_,1,_,1,_,_,_,_,_,1,_,_,_,_,1,_,1,1,1],
    [1,_,_,_,_,1,1,_,1,_,_,_,_,_,_,_,1,_,1,_,1,1,1,1,_,1,_,1,_,1],
    [1,1,_,1,1,1,1,_,_,_,1,1,1,_,1,_,1,_,1,_,1,_,_,1,_,1,_,_,_,1],
    [1,_,_,_,_,1,_,_,1,_,_,1,_,_,1,1,1,_,1,_,_,_,1,1,_,1,_,1,_,1],
    [1,1,1,_,1,1,1,_,1,1,_,_,_,1,1,_,_,_,1,_,1,_,_,_,_,1,_,1,_,1],
    [1,1,_,_,1,_,1,_,1,_,_,1,1,1,_,_,1,1,1,_,1,_,1,_,_,_,_,1,_,1],
    [1,1,1,_,1,_,_,_,1,1,_,1,_,1,_,1,1,1,1,_,1,1,1,1,1,_,1,1,1,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,1,_,_,_,_,_,_,1,_,_,_,_,_,_,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,_,1,1,1,_,1,1,1,1,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

for x in range(len(objectmap)):
    for y in range(len(objectmap[x])):
        if objectmap[x][y] == 1:
            objects.append(gameobject("Map",True,[100,100],[y*100,x*100],True,None,(255,255,255),0,0,None,False,1))

def moveobjects(xvel,yvel):
    totaloffset[0] -= xvel #Move the total offset values
    totaloffset[1] -= yvel
    for myobject in objects: #Moves all the objects. Used for screen shake effects
        try:
            myobject.position[0] + xvel
            myobject.position[1] + yvel
        except:
            print("Failed to Move Object:",myobject.name)

mousedown = False

def calculate_movement(speed,angle_in_radians):
    new_x = (speed*math.sin(angle_in_radians))
    new_y = (speed*math.cos(angle_in_radians))
    return new_x, new_y

gun = Weapon(1,5,15,1,1,0,120,None,3,1)

objects.insert(-1,gameobject("mapstart",True,[maptilesize,maptilesize],[mapstart[0]+maptilesize/2,mapstart[1]+maptilesize/2],False,None,(0,255,255),0,0,None,False,-1))
mymap = generatemap(maptilesize,mapwidth,mapheight,mapstart)
pathfinding = PathFinding(mymap)

pathfindupdate = 1

deltaseconds = 0

while True:
    # creating a loop to check events that
    # are occurring

    dt = clock.tick(maxfps)

    deltaseconds = dt/1000


    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousedown = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display.fill((128,128,128)) #Fill the background

    occupied_tiles = []
    collidableobj = []
    bulletcollidable = []
    team1,team1rects = [],[]
    team2,team2rects = [],[]

    for object in objects:
        if object.hascolisions and object.rect and object.transparency < 1:
            bulletcollidable.append(object.rect)

        if object.hascolisions and object.rect:
            collidableobj.append(object.rect)

        if object.name == "fps":
            object.customclass.text = str(int(clock.get_fps()))

        if isinstance(object.customclass,enemy):
            team2.append(object)
            team2rects.append(object.rect)
            occupied_tiles.append((object.customclass.myxpos,object.customclass.myypos))

        if isinstance(object.customclass,Player):
            team1.append(object)
            team1rects.append(object.rect)

    if mousedown:
        for object in objects:
            if isinstance(object.customclass,Player):
                gun.fire(object.rect.center)
    gun.update()

    objects.sort() # Sort the objects depending on their layer so that they render in the right order

    originallength = len(objects)

    if not GamePaused:
        for myobject in objects:
            if myobject.size and myobject.position:
                myobject.update()
                size = myobject.size
                pos = myobject.position
                if pos[0]+(size[0]/2) > 0 or pos[0]-(size[0]/2) < windowsize[0] or pos[1]+(size[1]/2) > 0 or pos[1]-(size[1]/2) < windowsize[1]:
                    myobject.visible = True
                else:
                    myobject.visible = False
                if isinstance(object.customclass,enemy):
                    team2rects.append(object.rect)
        for myobject in objects:
            if myobject.rect and myobject.visible:
                if myobject.transparency != 0:
                    if myobject.transparency >= 1:
                        continue
                    s = pygame.Surface((myobject.rect.width,myobject.rect.height))
                    s.set_alpha(255 - myobject.transparency*255)
                    s.fill(myobject.colour)
                    display.blit(s, (myobject.rect.x,myobject.rect.y))
                else:
                    renderrect(myobject.rect,display,myobject.colour)
                if isinstance(myobject.customclass,text):
                    newsurf,textrect = text_objects(myobject.customclass.text,myobject.customclass.finalfont,myobject.customclass.textcolour)
                    display.blit(newsurf,(myobject.rect.centerx-textrect.width/2,myobject.rect.centery-textrect.height/2))

    pathfindupdate -= (deltaseconds*gamespeed)
    if pathfindupdate <= 0:
        pathfindupdate = 5
        mymap = generatemap(maptilesize,mapwidth,mapheight,list(objects[0].rect.topleft))
        pathfinding.update(mymap)

    pygame.display.update() #Update the display to visualise all of the objects