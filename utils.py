import pygame as pg
from settings import *
from math import floor

class Map:
    def __init__(self, filename):
        self.data = []

        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data )
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        print ('map initialized ... ')

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x,y, width, height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet, (0,0),(x,y,width,height))
        new_image = pg.transform.scale(image, (width,height))
        image = new_image
        return image

class Cooldown:
    def __init__(self):
        self.starttime=0
        
        self.eventtime = 0
        self.currenttime=0
    def ticking(self):
        self.currenttime = floor ((pg.time.get_ticks())/1000)
        self.delta = self.currenttime - self.eventtime
    def start(self):
        self.starttime = pg.time.getticks()
    
