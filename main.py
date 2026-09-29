#this code is writen by peisho wang
# code inspired by chris bradfield who was inspired by notch

import pygame as pg
from os import path
from settings import *
from sprites import *
from utils import *
#imports the pygame, our game engine, very cool
#also imports everything from settings, another one of our files
# input (events): Keyboard, Mouse, right/left click, voice, power button, location, microphone
# Data types: boolean, interger, strings, JSON
#process: cursor position, position of player in game,score, enemy position, velocity, aim in fps \
# output: sounds, graphics, haptics, 

class Game:
    def __init__(self):
        #underscores mean special
        pg.init()
        #preps lots of game stuff like physics
        pg.mixer.init()
        #ititializes sound
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        print ("game initiallized...........")
        # prints to confirm that the code is running
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        #promps the program to start running
        self.clock = pg.time.Clock()

    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.map = Map(path.join(self.game_dir, map))

    def new(self):
        self.load_data('level1.txt')
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.cactus = Wall(self,10,10)
        # creates wall
        self.mob = Mob(self,10,5)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate (tiles):
                if tile == '1':
                    Wall(self, col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate (tiles):
                if tile == 'P':
                    Player(self, col,row)

        #creates the sprite groups and also adds the player

    def run(self):
        self.playing=True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.draw()
            self.update()
            #runs all of the programs
        #lets the program run the game window

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        #allows you to quit out of the code, everything is an event

    def update(self):
        self.all_sprites.update()
        #causes the sprite to update, updating to a new position
        if len(self.all_mobs) < 1:
            print ('out of mobs')
            self.mob = Mob(self,10,5)
        

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)  
        pg.display.flip()
        # sets the backround color and draws the sprites


if __name__ == "__main__":
    #makes sure the file is the main file
    g = Game()
    # sets g to game, allows us to run the game


while g.running:
    g.new()
    g.run()
    #gets the code to start running
    