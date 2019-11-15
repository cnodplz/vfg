#!/bin/python
import sys
import pygame
import random
import time
from colors import *
from pygame.locals import Color, KEYUP, KEYDOWN, K_ESCAPE, K_RETURN, K_w, K_a, K_s, K_d, K_i, K_q, K_LSHIFT
import spritesheet
from sprite_anim import SpriteStripAnim
import rpgdata

'''
    occasional setstats error when killing slimes
'''
class Block(pygame.sprite.Sprite):
    def __init__(self, color=orange_yellow, sp_width=64, sp_height=64):
        super(Block, self).__init__()
        self.image=pygame.Surface((sp_width,sp_height))
        self.image.fill(orange_yellow)
        self.rect=self.image.get_rect()
    def set_position(self, x, y):
        self.rect.x=x
        self.rect.y=y
    def set_image(self, filename=None):
        if (filename!=None):
            self.image=pygame.image.load(filename)
            self.rect=self.image.get_rect()
    def get_positionx(self):
        return self.rect.x
    def get_positiony(self):
        return self.rect.y
    def update_position(self, x, y):
        self.rect.x += x
        self.rect.y += y

class Console():
    def __init__(self, concolor=orange_yellow, conmsg="", x_pos=100, y_pos=100):
        self.concolor=concolor
        self.conmsg=conmsg
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.labelcon=confont.render(self.conmsg, 0, (self.concolor))
        self.labellist=[]
        self.labellist.append(self.labelcon)
        self.size=9
        self.fontsep=12

    def setit(self, concolor, conmsg, x_pos, y_pos):
        self.concolor=concolor
        self.conmsg=conmsg
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.labelcon=confont.render(self.conmsg, 0, (self.concolor))
        self.labellist.append(self.labelcon)

    def addmsg(self, conmsg):
        self.conmsg=conmsg
        self.labelcon=confont.render(self.conmsg, 0, (self.concolor))
        #self.labellist=[]
        self.labellist.append(self.labelcon)

    def setpos(self, x_pos, y_pos):
        self.x_pos=x_pos
        self.y_pos=y_pos

    def setsize(self, size):
        self.size=size

    def setfontsep(self, fontsep):
        self.fontsep=fontsep

    def setsingle(self, conmsg):
        self.conmsg=conmsg
        self.labelcon=confont.render(self.conmsg, 0, (self.concolor))
        self.labellist=[]
        self.labellist.append(self.labelcon)

    def drawit(self):
        tenplus=0
        #if len(self.labellist) > 9:
        if len(self.labellist) > self.size:
            del self.labellist[0]
        elif len(self.labellist) == 1:
            surface.blit(self.labellist[0], (self.x_pos,self.y_pos))
        else:
            for x in self.labellist:
                tenplus+=self.fontsep
                surface.blit(x, (self.x_pos,self.y_pos + tenplus))

class Erect():

    def __init__(self, lcolor=white, lcolor2=grey, x_pos=198, y_pos=148, x_size=104, y_size=54):
        self.lcolor=lcolor
        self.lcolor2=lcolor2
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.x_size=x_size
        self.y_size=y_size

    def setit(self, lcolor, lcolor2, x_pos, y_pos, x_size, y_size):
        self.lcolor=lcolor
        self.lcolor2=lcolor2
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.x_size=x_size
        self.y_size=y_size

    def setpos(self, x_pos, y_pos):
        self.x_pos=x_pos
        self.y_pos=y_pos

    def setcolor(self, lcolor, lcolor2):
        self.lcolor=lcolor
        self.lcolor=lcolor2

    def setsize(self, x_size, y_size):
        self.x_size=x_size
        self.y_size=y_size

    def drawit(self):
        pygame.draw.rect(surface, self.lcolor, (self.x_pos, self.y_pos, self.x_size, self.y_size))
        pygame.draw.rect(surface, self.lcolor2, (self.x_pos+2, self.y_pos+2, self.x_size-4, self.y_size-4))

class MTX():
    def __init__(self, tilemapsize=10, block_size=10, x_pos=0, y_pos=0):
        self.block_size=block_size
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.x_pos_list=[]
        self.x_arraypos_list=[]
        self.y_pos_list=[]
        self.y_arraypos_list=[]
        self.tilemapsize=tilemapsize
        self.tilemapcountx=self.x_pos
        self.tilemapcounty=self.y_pos
        self.blocky=[]
        self.list_x=[]
        self.list_y=[]
        self.block_counter=0
        for x in range(self.tilemapsize):
            self.x_pos_list.append(self.tilemapcountx)
            self.tilemapcountx+=self.block_size
            self.y_pos_list.append(self.tilemapcounty)
            self.tilemapcounty+=self.block_size
        self.x_arraypos_list=[[self.x_pos_list[x] for x in range(self.tilemapsize)] for x in range(self.tilemapsize)]
        self.y_arraypos_list=[[self.y_pos_list[x] for x in range(self.tilemapsize)] for x in range(self.tilemapsize)]
        # fill grid matrix of given size with randomized integers
        for row in range(self.tilemapsize):
            self.blocky.append([])
            for column in range(self.tilemapsize):
                self.blocky[row].append(random.randint(0,4))

    def randomize(self):
        self.blocky=[]
        for row in range(self.tilemapsize):
            self.blocky.append([])
            for column in range(self.tilemapsize):
                self.blocky[row].append(random.randint(0,4))

    def valuecheck(self):
        for x in range(self.tilemapsize):
            print("blocky: {}".format(self.blocky[x]))
        for x in range(self.tilemapsize):
            print("x_arraypos_list: {}".format(self.x_arraypos_list[x]))
        for x in range(self.tilemapsize):
            print("y_arraypos_list: {}".format(self.y_arraypos_list[x]))

    def drawit(self):
        for x in range(self.tilemapsize):
            for y in range(self.tilemapsize):
                if self.blocky[x][y] == 0:
                    pygame.draw.rect(surface, orange_yellow, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x], self.block_size, self.block_size))
                    # surface.blit(grass3, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x],self.block_size,self.block_size))
                elif self.blocky[x][y] == 1:
                    pygame.draw.rect(surface, intblue, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x], self.block_size, self.block_size))
                    # surface.blit(grass3, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x],self.block_size,self.block_size))
                elif self.blocky[x][y] == 2:
                    pygame.draw.rect(surface, dkgrey, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x], self.block_size, self.block_size))
                elif self.blocky[x][y] == 3:
                    pygame.draw.rect(surface, red, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x], self.block_size, self.block_size))
                elif self.blocky[x][y] == 4:
                    pygame.draw.rect(surface, lime, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x], self.block_size, self.block_size))
                    # surface.blit(grass3, (self.x_arraypos_list[x][y], self.y_arraypos_list[y][x],self.block_size,self.block_size))

class Attack():
    def __init__(self, x=0, y=0, polarity=1):
        self.block_size=5
        self.attack_w=[]
        self.attack_a=[]
        self.attack_s=[]
        self.attack_d=[]
        self.attack_w_posx=[]
        self.attack_w_posy=[]
        self.attack_a_posx=[]
        self.attack_a_posy=[]
        self.attack_s_posx=[]
        self.attack_s_posy=[]
        self.attack_d_posx=[]
        self.attack_d_posy=[]
        self.x_arraypos_list_w=[]
        self.y_arraypos_list_w=[]
        self.x_arraypos_list_a=[]
        self.y_arraypos_list_a=[]
        self.x_arraypos_list_s=[]
        self.y_arraypos_list_s=[]
        self.x_arraypos_list_d=[]
        self.y_arraypos_list_d=[]
        self.posx=x
        self.posy=y
        self.polarity=polarity
        self.tilemapsizex=7
        self.tilemapsizey=4
        self.tilemapcountx=x
        self.tilemapcounty=y
        self.attack_w.append([1,1,1,1,1,1,1])
        self.attack_w.append([0,1,1,1,1,1,0])
        self.attack_w.append([0,0,1,1,1,0,0])
        self.attack_w.append([0,0,0,1,0,0,0])
        self.attack_a.append([1,0,0,0])
        self.attack_a.append([1,1,0,0])
        self.attack_a.append([1,1,1,0])
        self.attack_a.append([1,1,1,1])
        self.attack_a.append([1,1,1,0])
        self.attack_a.append([1,1,0,0])
        self.attack_a.append([1,0,0,0])
        self.attack_s.append([0,0,0,1,0,0,0])
        self.attack_s.append([0,0,1,1,1,0,0])
        self.attack_s.append([0,1,1,1,1,1,0])
        self.attack_s.append([1,1,1,1,1,1,1])
        self.attack_d.append([0,0,0,1])
        self.attack_d.append([0,0,1,1])
        self.attack_d.append([0,1,1,1])
        self.attack_d.append([1,1,1,1])
        self.attack_d.append([0,1,1,1])
        self.attack_d.append([0,0,1,1])
        self.attack_d.append([0,0,0,1])

    def setpos(self, x, y):
        self.tilemapcountx=x
        self.tilemapcounty=y
        # tilemapsizex=7
        for x in range(self.tilemapsizex):
            self.attack_w_posx.append(self.tilemapcountx)
            self.attack_w_posy.append(self.tilemapcounty)
            self.attack_s_posx.append(self.tilemapcountx)
            self.attack_s_posy.append(self.tilemapcounty)
            self.tilemapcountx+=self.block_size*2
        # tilemapsizey=4
        for x in range(self.tilemapsizey):
            self.attack_a_posx.append(self.tilemapcountx)
            self.attack_d_posx.append(self.tilemapcountx)
            self.tilemapcountx+=self.block_size*2
        # tilemapsizex=7
        for x in range(self.tilemapsizex):
            self.attack_a_posy.append(self.tilemapcounty)
            self.attack_d_posy.append(self.tilemapcounty)
            self.tilemapcounty+=self.block_size*2

        self.x_arraypos_list_w=[[self.attack_w_posx[x] for x in range(self.tilemapsizex)] for x in range(self.tilemapsizey)]
        self.y_arraypos_list_w=[[self.attack_w_posy[x] for x in range(self.tilemapsizex)] for x in range(self.tilemapsizey)]
        self.x_arraypos_list_a=[[self.attack_a_posx[x] for x in range(self.tilemapsizey)] for x in range(self.tilemapsizex)]
        self.y_arraypos_list_a=[[self.attack_a_posy[x] for x in range(self.tilemapsizey)] for x in range(self.tilemapsizex)]
        self.x_arraypos_list_s=[[self.attack_s_posx[x] for x in range(self.tilemapsizex)] for x in range(self.tilemapsizey)]
        self.y_arraypos_list_s=[[self.attack_s_posy[x] for x in range(self.tilemapsizex)] for x in range(self.tilemapsizey)]
        self.x_arraypos_list_d=[[self.attack_d_posx[x] for x in range(self.tilemapsizey)] for x in range(self.tilemapsizex)]
        self.y_arraypos_list_d=[[self.attack_d_posy[x] for x in range(self.tilemapsizey)] for x in range(self.tilemapsizex)]
        self.tilemapcountx=0
        self.tilemapcounty=0
        self.attack_w_posx=[]
        self.attack_w_posy=[]
        self.attack_a_posx=[]
        self.attack_a_posy=[]
        self.attack_s_posx=[]
        self.attack_s_posy=[]
        self.attack_d_posx=[]
        self.attack_d_posy=[]

    def setpolarity(self, polarity=1):
        self.polarity=polarity

    def drawit(self):
        if self.polarity==1:
            for x in range(self.tilemapsizey):
                for y in range(self.tilemapsizex):
                    if self.attack_w[x][y]==1:
                        pygame.draw.rect(surface, red, (self.x_arraypos_list_w[x][y], self.y_arraypos_list_w[x][y], 5, 5))
                    elif self.attack_w[x][y]==0:
                        pygame.draw.rect(surface, dkgrey, (self.x_arraypos_list_w[x][y], self.y_arraypos_list_w[x][y], 5, 5))
        if self.polarity==2:
            for x in range(self.tilemapsizex):
                for y in range(self.tilemapsizey):
                    if self.attack_a[x][y]==1:
                        pygame.draw.rect(surface, red, (self.x_arraypos_list_a[x][y], self.y_arraypos_list_a[x][y], 5, 5))
                    elif self.attack_a[x][y]==0:
                        pygame.draw.rect(surface, dkgrey, (self.x_arraypos_list_a[x][y], self.y_arraypos_list_a[x][y], 5, 5))
        if self.polarity==3:
            for x in range(self.tilemapsizey):
                for y in range(self.tilemapsizex):
                    if self.attack_s[x][y]==1:
                        pygame.draw.rect(surface, red, (self.x_arraypos_list_s[x][y], self.y_arraypos_list_s[x][y], 5, 5))
                    elif self.attack_s[x][y]==0:
                        pygame.draw.rect(surface, dkgrey, (self.x_arraypos_list_s[x][y], self.y_arraypos_list_s[x][y], 5, 5))
        if self.polarity==4:
            for x in range(self.tilemapsizex):
                for y in range(self.tilemapsizey):
                    if self.attack_d[x][y]==1:
                        pygame.draw.rect(surface, red, (self.x_arraypos_list_d[x][y], self.y_arraypos_list_d[x][y], 5, 5))
                    elif self.attack_d[x][y]==0:
                        pygame.draw.rect(surface, dkgrey, (self.x_arraypos_list_d[x][y], self.y_arraypos_list_d[x][y], 5, 5))

    def valuecheck(self):
        print("attack_w_posx: {}".format(self.attack_w_posx))
        print("attack_w_posy: {}".format(self.attack_w_posy))
        print("x_arraypos_list_w: {}".format(self.x_arraypos_list_w))
        print("y_arraypos_list_w: {}".format(self.y_arraypos_list_w))
        print("x_arraypos_list_a: {}".format(self.x_arraypos_list_a))
        print("y_arraypos_list_a: {}".format(self.y_arraypos_list_a))
        print("x_arraypos_list_s: {}".format(self.x_arraypos_list_s))
        print("y_arraypos_list_s: {}".format(self.y_arraypos_list_s))
        print("x_arraypos_list_d: {}".format(self.x_arraypos_list_d))
        print("y_arraypos_list_d: {}".format(self.y_arraypos_list_d))

def startscreen(controller):
    #window_sizex=window_widthx, window_heightx=1600,900
    #surfacex=pygame.display.set_mode(window_size,pygame.RESIZABLE)
    surface.fill(dkgrey)
    start_x,start_y = pygame.mouse.get_pos()
    start_x1,start_y1 = window_width/2-40,window_height/2-200
    startcon1=startfont.render("START", 0, (black))
    startcon2=startfont.render("SAVE", 0, (black))
    startcon3=startfont.render("QUIT", 0, (black))
    pygame.draw.rect(surface, red, (start_x1, start_y1, 200, 180))
 
    if start_x >= start_x1 and start_x <= start_x1 + 200:
        if start_y >= start_y1 and start_y <= start_y1+60:   
            startcon1=startfont.render("START", 0, (white))
    else:
            startcon1=startfont.render("START", 0, (black))

    if start_x >= start_x1 and start_x <= start_x1 + 200:
        if start_y >= start_y1+60 and start_y <= start_y1+120:   
            startcon2=startfont.render("SAVE", 0, (white))
    else:
            startcon2=startfont.render("SAVE", 0, (black))

    if start_x >= start_x1 and start_x <= start_x1 + 200:
        if start_y >= start_y1+120 and start_y <= start_y1+180:   
            startcon3=startfont.render("QUIT", 0, (white))
    else:
            startcon3=startfont.render("QUIT", 0, (black))

    surface.blit(startcon1, (window_width/2-25, window_height/2-200))
    surface.blit(startcon2, (window_width/2-25, window_height/2-140))
    surface.blit(startcon3, (window_width/2-25, window_height/2-80))

def ranmove(x):
    randseed=random.randint(1,4)
    if randseed==1:
        x=-x
        return x
    elif randseed==2:
        x=x
        return x
    elif randseed==3:
        x=-x
        return x
    elif randseed==4:
        x=x
        return x
        
# Set window size, default surface, FPS
window_size=window_width, window_height=1600,900
#cabinx,cabiny=400,200
controller=1
surface=pygame.display.set_mode(window_size,pygame.RESIZABLE)
surface.fill(dkgrey)
#cabin = pygame.Surface((cabinx,cabiny))
#cabin.fill(black)
# transparent surface ui
ui_bar_1 = pygame.Surface((1600,100)) # the size of your rect
ui_bar_1.set_alpha(128) # alpha level
ui_bar_1.fill((10,10,10)) # this fills the entire surface
FPS = 60
frames = FPS / 6

# Animated sprites
strips=[
    SpriteStripAnim('rain1.gif', (0,0,200,200), 4, 1, True, frames)
    ]
char_walk_w=[
    SpriteStripAnim('char_walk_w3.png', (0,0,38,62), 4, 1, True, frames)
    #SpriteStripAnim('char_walk_w_sponge.png', (0,0,64,64), 4, 1, True, frames)
    ]
char_walk_a=[
    SpriteStripAnim('char_walk_a3.png', (0,0,35,62), 4, 1, True, frames)
    #SpriteStripAnim('char_walk_a_sponge.png', (0,0,64,64), 4, 1, True, frames)
    ]
char_walk_s=[
    SpriteStripAnim('char_walk_s3.png', (0,0,38,64), 4, 1, True, frames)
    #SpriteStripAnim('char_walk_s_sponge.png', (0,0,64,64), 4, 1, True, frames)
    ]
char_walk_d=[
    SpriteStripAnim('char_walk_d3.png', (0,0,35,63), 4, 1, True, frames)
    #SpriteStripAnim('char_walk_d_sponge2.png', (0,0,64,64), 4, 1, True, frames)
    ]

# block groups and sprites
#block_group=pygame.sprite.Group()
block_group1=pygame.sprite.LayeredUpdates()
block_group2=pygame.sprite.LayeredUpdates()
block_group3=pygame.sprite.LayeredUpdates()
a_block=Block()
a_block.set_image("forest2.jpg")
a_block.set_position(0, 0)
b_block=Block()
b_block.set_image("console.gif")
b_block.set_position(window_width/2 - 300, window_height/2 + 100)
c_block=Block()
c_block.set_image("console_main.gif")
c_block.set_position(window_width/2 - 300, window_height/2 - 260)
d_block=Block()
d_block.set_image("skware64.png")
d_block.set_position(10, window_height-74)
e_block=Block()
e_block.set_image("skware64.png")
e_block.set_position(84, window_height-74)
f_block=Block()
f_block.set_image("skware64.png")
f_block.set_position(158, window_height-74)
g_block=Block()
g_block.set_image("skware64.png")
g_block.set_position(232, window_height-74)
h_block=Block()
h_block.set_image("swd_x_w.png")
i_block=Block()
i_block.set_image("swd_x_a.png")
j_block=Block()
j_block.set_image("swd_x_s.png")
k_block=Block()
k_block.set_image("swd_x_d.png")
red_slime=Block()
green_slime=Block()
blue_slime=Block()
red_slime.set_image("slime_red_s.png")
green_slime.set_image("slime_green_s.png")
blue_slime.set_image("slime_blue_s.png")
red_slime.set_position(window_width/2,window_height/2)
green_slime.set_position(window_width/2,window_height/2)
blue_slime.set_position(window_width/2,window_height/2)
block_group1.add(d_block,e_block,f_block,g_block)
block_group2.add(red_slime,green_slime,blue_slime)
#block_group3.add(h_block,i_block,j_block,k_block)

# images
grass1=pygame.image.load("skware64.png")
grass2=pygame.image.load("grass2.jpg")
water1=pygame.image.load("water2.png")
grass2=pygame.transform.scale(grass2,(32,32))
grass3=pygame.transform.scale(grass2,(20,20))
redpot=pygame.image.load("redpot.png")
greenpot=pygame.image.load("greenpot.png")
bluepot=pygame.image.load("bluepot.png")
yellowpot=pygame.image.load("yellowpot.png")
swd_x=pygame.image.load("swd_x.png")
char_default = pygame.image.load("rag_char_1.png")
grass1=pygame.image.load("skware64.png")
grass2=pygame.image.load("grass2.jpg")
water1=pygame.image.load("water2.png")
grass2=pygame.transform.scale(grass2,(32,32))
char_default = pygame.image.load("rag_char_1.png")
#map_default = pygame.image.load("grass1.png")
#map_default = pygame.image.load("city2.png")
map_default = pygame.image.load("forest2.jpg")
map_default2 = pygame.image.load("a_map.png")
#map_cabin1 = pygame.image.load("map_cabin2.png")
map_scale1 = pygame.transform.scale(map_default, (1600, 900))
#map_cabin_scale1 = pygame.transform.scale(map_cabin1,(cabinx,cabiny))

# initialization game text consoles, blit
surface.blit(map_scale1, (0, 0))
#surface.blit(map_default2, (0, 0))
#cabin.blit(map_cabin1, (0,0))
font_size_1=12
font_size_2=48
pygame.font.init()
confont=pygame.font.Font("/usr/share/fonts/google-droid/DroidSansMono.ttf", font_size_1)
startfont=pygame.font.Font("/usr/share/fonts/google-droid/DroidSansMono.ttf", font_size_2)
#label=confont.render("Random Encounter!", False, (red))
gameconsole = Console()
gameconsole.setsize(6)
gameconsole.setit(red,"Initialize: {}".format("Random Encounter!"),50,0)
gameconsole.addmsg("Item!")
gameconsole.addmsg("Slime!")
gameconsole.addmsg("Sword!")
gameconsole.addmsg("Enemy!")

# variables
clock = pygame.time.Clock()
n=0
tilemapsize=10
block_size=10
strips[n].iter()
char_walk_w[n].iter()
char_walk_a[n].iter()
char_walk_s[n].iter()
char_walk_d[n].iter()
image = strips[n].next()
image1 = char_walk_w[n].next()
image2 = char_walk_a[n].next()
image3 = char_walk_s[n].next()
image4 = char_walk_d[n].next()
#tilemap1=[[random.randint(0,4) for x in range(tilemapsize)] for x in range(tilemapsize)]
blocky3=[]
list_x=[]
list_y=[]
square_x=30
square_y=30
last_player_direction=0
player_pos_x=window_width/2
player_pos_y=window_height/2
player1=rpgdata.player("P1")
player1.setnerd("P2", "C1", 1, 100, 100)
player1.stats()
player2=rpgdata.player("P2")
player2.setnerd("P2", "C2", 1, 200, 200)
player2.stats()
#monster1=rpgdata.monster(random.randint(1,12))
monster1=rpgdata.monster(random.randint(1,12))
monster2=rpgdata.monster(random.randint(1,12))
monster3=rpgdata.monster(random.randint(1,12))
playerconsole=Console()
playerstats=Console()
monsterconsole1=Console()
monsterconsole2=Console()
monsterconsole3=Console()
playerstats=Console()
playerconsole.setit(green, "[ {} {}/{} ]".format(str(player1.name), player1.life, player1.life), player_pos_x-30, player_pos_y+40)
playerstats.setit(orange_yellow,"name: {} job: {} hp: {} mana: {} attack: {}".format(player1.name,player1.job,player1.life,player1.mana,player1.atk),window_width-600,10)
monsterconsole1.setit(orange_yellow, "[ {} {}/{} ]".format(str(monster1.mon_name), str(monster1.mon_hp-monster1.mon_dmgtaken), str(monster1.mon_hp)), player_pos_x, player_pos_y)
monsterconsole2.setit(orange_yellow, "[ {} {}/{} ]".format(str(monster2.mon_name), str(monster2.ehealth), str(monster2.mon_hp)), player_pos_x, player_pos_y)
monsterconsole3.setit(orange_yellow, "[ {} {}/{} ]".format(str(monster3.mon_name), str(monster3.mon_hp-monster3.mon_dmgtaken), str(monster3.mon_hp)), player_pos_x, player_pos_y)
p1_inv=rpgdata.inventory()
inventoryon=0
invconsole=Console()
invconsole.setsize(20)
invconsole.setfontsep(16)
invconsole.setit(white,"",window_width/2-380,window_height/2-300)
monsterwalk=0
monsterwalk1=0
inventorycount=0

# static logic
cube1=MTX(tilemapsize=20, block_size=5, x_pos=window_width-100, y_pos=0)
last_time=time.time()
last_swd_time=time.time()
testattack=Attack()
testattackvector=0
nameplate1=Erect()
nameplate1.setcolor(dkgrey,black)
nameplate1.setsize(150,20)
nameplate2=Erect()
nameplate2.setcolor(dkgrey,black)
nameplate2.setsize(150,20)
nameplate3=Erect()
nameplate3.setcolor(dkgrey,black)
nameplate3.setsize(150,20)
nameplate4=Erect()
nameplate4.setcolor(dkgrey,black)
nameplate4.setsize(150,20)
invwindow=Erect()
invwindow.setcolor(dkgrey,red)
invwindow.setsize(800,400)
invwindow.setpos(window_width/2-400,window_height/2-300)
last_monster_direction=0
monmove4=0
monmove2=random.randint(1,4)
last_mons_time=time.time()

# main game loop
while True:

    # Initial surfaces
    surface.blit(map_scale1, (0,0))
    surface.blit(ui_bar_1, (0,0))
    #surface.blit(cabin, (window_width-cabinx, window_height-cabiny))

    # Set initial variables
    key_state = pygame.key.get_pressed()

    # Monster movement
    if time.time()-last_time > .5:
        monmove4+=1
        if monmove2==1:
            red_slime.update_position(0,-monmove4)
            green_slime.update_position(0,-monmove4)
            blue_slime.update_position(monmove4,0)
        if monmove2==2:
            red_slime.update_position(-monmove4,0)
            green_slime.update_position(0,-monmove4)
            blue_slime.update_position(monmove4,0)
        if monmove2==3:
            red_slime.update_position(0,monmove4)
            green_slime.update_position(0,-monmove4)
            blue_slime.update_position(-monmove4,0)
        if monmove2==4:
            red_slime.update_position(monmove4,0)
            green_slime.update_position(0,-monmove4)
            blue_slime.update_position(-monmove4,0)
        #green_slime.update_position(random.randint(-20,20), random.randint(-20,20))
        #blue_slime.update_position(monmove3, 0)
        last_time = time.time()
    monmove4=0

    # Keys and events
    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                sys.exit()
            elif e.key == K_RETURN:
                pass
            elif e.key == K_i:
                if inventoryon==0:
                    p1_inv.additem(random.randint(1,15))
                    inventoryon=1
                    inventorycounter=1
                    for aa in p1_inv.inventory_list:
                        invconsole.addmsg("[{}] {}".format(inventorycounter, p1_inv.getitem(aa)))
                        inventorycounter+=1
                    invwindow.drawit()
                    inventorycounter=1
                elif inventoryon==1:
                    inventoryon=0
                print(p1_inv.inventory_list)
            elif e.key == K_q:
                controller=0

        if e.type == pygame.MOUSEBUTTONDOWN:
            cube1.randomize()
            #cube1.valuecheck()
            print(monster1.ehealth)
            print(monster2.ehealth)
            print(monster3.ehealth)
            start_x,start_y = pygame.mouse.get_pos()
            start_x1,start_y1 = window_width/2-50,window_height/2-200
            if start_x >= start_x1 and start_x <= start_x1 + 200:
                if start_y >= start_y1 and start_y <= start_y1+60:
                    controller=0
            if start_x >= start_x1 and start_x <= start_x1 + 200:
                if start_y >= start_y1+120 and start_y <= start_y1+180:
                    sys.exit()

            if last_player_direction==1:
                testattack.setpos(player_pos_x,player_pos_y)
                testattack.setpolarity(last_player_direction)
                testattackvector=1
                testattack.valuecheck()
                h_block.set_image("swd_x2_w.png")
                h_block.set_position(player_pos_x+20,player_pos_y-144)
                block_group3.add(h_block)
                last_swd_time=time.time()
                # check hit collision and effective health <= 0, maybe better outside of direction logic
                for x in block_group2:
                    if pygame.sprite.collide_rect(h_block, x) == True:
                        for y in monster1, monster2, monster3:
                            if y.ehealth<=0:
                                last_x,last_y=x.get_positionx(),x.get_positiony()
                                x.set_image("blud2.png")
                                x.set_position(last_x,last_y)
                                last_mons_time=time.time()
                                player1.setstats(random.randint(1,20))
                            else:
                                y.atk_monster(player1.atk)

            if last_player_direction==2:
                testattack.setpos(player_pos_x,player_pos_y)
                testattack.setpolarity(last_player_direction)
                testattackvector=1
                testattack.valuecheck()
                h_block.set_image("swd_x2_a.png")
                h_block.set_position(player_pos_x-144,player_pos_y+30)
                block_group3.add(h_block)
                last_swd_time=time.time()
                for x in block_group2:
                    if pygame.sprite.collide_rect(h_block, x) == True:
                        for y in monster1, monster2, monster3:
                            if y.ehealth<=0:
                                last_x,last_y=x.get_positionx(),x.get_positiony()
                                x.set_image("blud2.png")
                                x.set_position(last_x,last_y)
                                last_mons_time=time.time()
                                player1.setstats(random.randint(1,20))
                            else:
                                y.atk_monster(player1.atk)

            if last_player_direction==3:
                testattack.setpos(player_pos_x,player_pos_y)
                testattack.setpolarity(last_player_direction)
                testattackvector=1
                testattack.valuecheck()
                h_block.set_image("swd_x2_s.png")
                h_block.set_position(player_pos_x+20,player_pos_y+72)
                block_group3.add(h_block)
                last_swd_time=time.time()
                for x in block_group2:
                    if pygame.sprite.collide_rect(h_block, x) == True:
                        for y in monster1, monster2, monster3:
                            if y.ehealth<=0:
                                last_x,last_y=x.get_positionx(),x.get_positiony()
                                x.set_image("blud2.png")
                                x.set_position(last_x,last_y)
                                last_mons_time=time.time()
                                player1.setstats(random.randint(1,20))
                            else:
                                y.atk_monster(player1.atk)

            if last_player_direction==4:
                testattack.setpos(player_pos_x,player_pos_y)
                testattack.setpolarity(last_player_direction)
                testattackvector=1
                testattack.valuecheck()
                h_block.set_image("swd_x2_d.png")
                h_block.set_position(player_pos_x+40,player_pos_y+30)
                block_group3.add(h_block)
                last_swd_time=time.time()
                for x in block_group2:
                    if pygame.sprite.collide_rect(h_block, x) == True:
                        for y in monster1, monster2, monster3:
                            if y.ehealth<=0:
                                last_x,last_y=x.get_positionx(),x.get_positiony()
                                x.set_image("blud2.png")
                                x.set_position(last_x,last_y)
                                last_mons_time=time.time()
                                player1.setstats(random.randint(1,20))
                            else:
                                y.atk_monster(player1.atk)

    # Use a key_state variable TRUE to catch when key is being pressed
    if key_state[K_w]:
        last_player_direction = 1
        image1 = char_walk_w[n].next()
        image1.set_alpha(255)
        image1.set_colorkey(0,0)
        player_pos_y+=-2
        playerconsole.setpos(player_pos_x-30,player_pos_y+40)
        nameplate4.setpos(player_pos_x-30,player_pos_y+40)

    if key_state[K_a]:
        last_player_direction = 2
        image2 = char_walk_a[n].next()
        image2.set_alpha(255)
        image2.set_colorkey(0,0)
        player_pos_x+=-2
        playerconsole.setpos(player_pos_x-30,player_pos_y+40)
        nameplate4.setpos(player_pos_x-30,player_pos_y+40)

    if key_state[K_s]:
        last_player_direction = 3
        image3 = char_walk_s[n].next()
        image3.set_alpha(255)
        image3.set_colorkey(0,0)
        player_pos_y+=2
        playerconsole.setpos(player_pos_x-30,player_pos_y+40)
        nameplate4.setpos(player_pos_x-30,player_pos_y+40)

    if key_state[K_d]:
        last_player_direction = 4
        image4 = char_walk_d[n].next()
        image4.set_alpha(255)
        image4.set_colorkey(0,0)
        player_pos_x+=2
        playerconsole.setpos(player_pos_x-30,player_pos_y+40)
        nameplate4.setpos(player_pos_x-30,player_pos_y+40)

    if key_state[K_LSHIFT]:
        if last_player_direction == 1:
            player_pos_y+=-3
            playerconsole.setpos(player_pos_x-30,player_pos_y+40)
            nameplate4.setpos(player_pos_x-30,player_pos_y+40)
        if last_player_direction == 2:
            player_pos_x+=-3
            playerconsole.setpos(player_pos_x-30,player_pos_y+40)
            nameplate4.setpos(player_pos_x-30,player_pos_y+40)
        if last_player_direction == 3:
            player_pos_y+=3
            playerconsole.setpos(player_pos_x-30,player_pos_y+40)
            nameplate4.setpos(player_pos_x-30,player_pos_y+40)
        if last_player_direction == 4:
            player_pos_x+=3
            playerconsole.setpos(player_pos_x-30,player_pos_y+40)
            nameplate4.setpos(player_pos_x-30,player_pos_y+40)

    # Draw block group1
    #block_group1.draw(surface)
    block_group2.draw(surface)
    #block_group3.draw(surface)
    nameplate1.setpos(red_slime.get_positionx()-20,red_slime.get_positiony()+50)
    nameplate2.setpos(green_slime.get_positionx()-20,green_slime.get_positiony()+50)
    nameplate3.setpos(blue_slime.get_positionx()-20,blue_slime.get_positiony()+50)
    nameplate4.setpos(player_pos_x-30,player_pos_y+60)
    monsterconsole1.setpos(red_slime.get_positionx()-20,red_slime.get_positiony()+50)
    monsterconsole2.setpos(green_slime.get_positionx()-20,green_slime.get_positiony()+50)
    monsterconsole3.setpos(blue_slime.get_positionx()-20,blue_slime.get_positiony()+50)
    monsterconsole1.setsingle("[ {} {}/{} ]".format(str(monster1.mon_name), str(monster1.ehealth), str(monster1.mon_hp)))
    monsterconsole2.setsingle("[ {} {}/{} ]".format(str(monster2.mon_name), str(monster2.ehealth), str(monster2.mon_hp)))
    monsterconsole3.setsingle("[ {} {}/{} ]".format(str(monster3.mon_name), str(monster3.ehealth), str(monster3.mon_hp)))
    playerstats.setsingle("name: {} level: {} xp: {} job: {} hp: {} mana: {} attack: {}".format(player1.name,player1.level,player1.xp1,player1.job,player1.life,player1.mana,player1.atk))

    if monster1.ehealth>0:
        nameplate1.drawit()
        monsterconsole1.drawit()
    if monster2.ehealth>0:
        nameplate2.drawit()
        monsterconsole2.drawit()
    if monster3.ehealth>0:
        nameplate3.drawit()
        monsterconsole3.drawit()
    if monster1.ehealth<=0:
        if time.time()-last_mons_time > 1:
            block_group2.remove(red_slime)
    if monster2.ehealth<=0:
        if time.time()-last_mons_time > 1:
            block_group2.remove(green_slime)
    if monster3.ehealth<=0:
        if time.time()-last_mons_time > 1:
            block_group2.remove(blue_slime)

    nameplate4.drawit()
    playerconsole.drawit()

    # Draw sprites
    #image = strips[n].next()  rain
    #surface.blit(image,(0,0))  rain
    #cabin.fill(black)
    #cabin.blit(map_cabin1,(0,0))
    if last_player_direction == 1:
        surface.blit(image1,(player_pos_x,player_pos_y))
        playerconsole.drawit()
    if last_player_direction == 2:
        surface.blit(image2,(player_pos_x,player_pos_y))
        playerconsole.drawit()
    if last_player_direction == 3:
        surface.blit(image3,(player_pos_x,player_pos_y))
        playerconsole.drawit()
    if last_player_direction == 4:
        surface.blit(image4,(player_pos_x,player_pos_y))
        playerconsole.drawit()
    #cabin.blit(redpot,(cabinx-300,cabiny-50))
    #cabin.blit(greenpot,(cabinx-250,cabiny-50))
    #cabin.blit(bluepot,(cabinx-200,cabiny-50))
    #cabin.blit(yellowpot,(cabinx-150,cabiny-50))
    #cabin.blit(swd_x,(cabinx-50,cabiny-100))
    cube1.drawit()
    if inventoryon==1:
        invwindow.drawit()
        invconsole.drawit()
    if testattackvector==1:
        if time.time()-last_swd_time < .5:
            testattack.drawit()
            block_group3.draw(surface)

    # Draw text
    #surface.blit(label, (100,600))
    gameconsole.drawit()
    playerstats.drawit()
    if controller != 0:
        startscreen(controller)
    
    pygame.display.update()
    clock.tick(FPS)
