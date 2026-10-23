#this code is writen by peisho wang
# code inspired by chris bradfield who was inspired sssby notch

import pygame as pg
from os import path
from settings import *
from sprites import *
from utils import *
import random as r

#imports the pygame, our game engine, very cool
#also imports everything from settings, another one of our files
# input (events): Keyboard, Mouse, right/left click, voice, power button, location, microphone
# Data types: boolean, interger, strings, JSON
#process: cursor position, position of player in game,score, enemy position, velocity, aim in fps \
# output: sounds, graphics, haptics, 
#ooh i changed something

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
        #fetches the name of the map file
        self.img_dir = path.join(self.game_dir, 'images')
        #fetches the images foldr
        self.snd_dir = path.join(self.game_dir, 'audio')
        #fetches the audio folder
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir,"metalClick.ogg"))
        # sound handeling
        self.map = Map(path.join(self.game_dir, map))
        #fetches the map 

    def new(self):
        self.load_data('level1.txt')
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_collectables = pg.sprite.Group()
        self.all_ores = pg.sprite.Group()
        # puts all the sprites in groups so twe can give the groups properties
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate (tiles):
                if tile == '1':
                    ore = r.randint(1,15)
                    if ore == 1:
                        Ores(self,col,row,'iron')
                    else:
                        Wall(self,col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate (tiles):
                if tile == 'P':
                    self.player = Player(self, col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate (tiles):
                if tile == 'E':
                    Mob(self, col,row)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate (tiles):
                if tile == 'B':
                    Collectable(self, col,row,'battery')
        # checks the tile map for the characters and makes things based on the characters

        #reads the map text in order to put everything in the right place

    def run(self):
        self.playing=True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            #sets the frame rate
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
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        #sets the font to arial
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        #sets to color and what text there is
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        # sets the position
        self.screen.blit(text_surface,text_rect)
                #puts the thing where it is supposed to be

    def update(self):
        self.all_sprites.update()
        #causes the sprite to update, updating to a new position
        
        

    def draw(self):
        self.screen.fill(DGRAY)
        self.all_sprites.draw(self.screen)  
        self.draw_text("Frames per second: "+ str(floor(1/self.dt)), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(f"Coins: {self.player.coins}",24, WHITE, WIDTH/2, HEIGHT/6)
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
    