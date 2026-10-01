# sprites are graphic entities in a game
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *

from os import path

vec = pg.math.Vector2
# imports a bunch of stuff that we are going to use
def collide_hit_rect(one,two):
     return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
     #checks sprite collision
     if dir == 'x':
        #checks collision on x axis
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
            #the first hit that we hit
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2
            if hits[0].rect.centerx<sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right+sprite.hit_rect.width/2
        sprite.vel=0
        sprite.hit_rect.centerx = sprite.pos.x
        
               
         
     if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
            #the first hit that we hit
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2                    
            if hits[0].rect.centery<sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom +sprite.hit_rect.height/2            
            sprite.vel=0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite):
    def __init__(self, game, x, y):
        #init runs only once at the start
        self.groups = game.all_sprites
        # gets game class into this code
        Sprite.__init__(self, self.groups)
        self.game = game
        # sets the game = to game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        #adds the spritesheet
        self.load_images()
        #allows the animations to load
        self.image = pg.Surface((TILESIZE,TILESIZE))
        # sets the image size to the size of the time
        self.image = self.spritesheet.get_image(0,0, TILESIZE, TILESIZE)
        #sets the image of the player
        #removes the color white
        self.rect = self.image.get_rect()
        #sets the shape to a rectangle
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        # sets the size fo the pixel, the color, and the position and velocity
        self.last_update = 0
        self.current_frame = 0
        #sets some animation things
        print('player initialized...')
        print(self.rect.x)
        print(self.rect.y)
        if self.vel.x != 0  and self.vel.y != 0:
            self.vel *=0.7071
        self.image.set_colorkey((255,255,255))

    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            
        self.image.set_colorkey((255,255,255))
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE*2,0,TILESIZE,TILESIZE),
                            self.spritesheet.get_image(TILESIZE*3,0,TILESIZE,TILESIZE),]
    def get_keys(self):
        #reset v to 0
        self.vel = vec(0,0)
        #listen for events specific to keys
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            #print('trying to go left')
            self.vel.x=-PLAYER_SPEED
            #self.vx=-PLAYER_SPEED
            #allows for the player to go left using the a or left keys

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            #print('trying to go right')
            self.vel.x=PLAYER_SPEED
            #self.vx=PLAYER_SPEED
            #allows the player to go right using the right or d keys

        if keys[pg.K_UP] or keys[pg.K_w]:
            #print('trying to go up')
            self.vel.y=-PLAYER_SPEED
            #self.vy=PLAYER_SPEED
            #allows the palyer to go up using the w or up keys, it is reverse for some reason

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            #print('trying to go down')
            self.vel.y=PLAYER_SPEED
            #self.vy=-PLAYER_SPEED
            #print (self.y)
            #allows the player to go down using the down or s key, is also reverse
        if self.vel.x != 0  and self.vel.y != 0:
             self.vel *=0.7071
        
        #change velocity based on which key is pressed
    def update(self):
        
        self.get_keys()
        #gets the keys so we can collect inputs
        self.animate()
        self.rect.center=self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx=self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center



class Wall(Sprite):
        
        def __init__(self, game, x, y):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_walls
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE,TILESIZE))
                # sets the image size to the size of the time
                self.image.fill(GREEN)
                #makes the color white
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.x = x*TILESIZE
                self.y = y*TILESIZE
                self.rect.x = self.x
                self.rect.y = self.y
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)

class Mob(Sprite):
        def __init__(self, game, x, y):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_mobs
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE,TILESIZE))
                # sets the image size to the size of the time
                self.image.fill(RED)
                #makes the color white
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 1,1
                self.x = x*TILESIZE
                self.y = y*TILESIZE
                self.rect.x = self.x
                self.rect.y = self.y
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                print('mob initialized...')
                print(self.rect.x)
                print(self.rect.y)
                self.speed = ENEMY_SPEED
        def update(self):
            pass

            if (self.x >= WIDTH-TILESIZE):
                print ('crossing +x border')
                self.vx = -1
            
            if (self.x <= 0):
                print ('crossing -x border')
                self.vx*=-1

            if (self.y >= HEIGHT-TILESIZE):
                print ('crossing -y border')
                self.vy*=-1
                
            if (self.y <= 0):
                print ('crossing +y border')
                self.vy*=-1
            
            self.x += self.vx*self.game.dt*self.speed
            self.y -= self.vy*self.game.dt*self.speed

            self.rect.x = self.x
            self.rect.y = self.y
