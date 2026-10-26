# sprites are graphic entities in a game
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from random import randint

from os import path

vec = pg.math.Vector2
# imports a bunch of stuff that we are going to use
def collide_hit_rect(one,two):
     return one.hit_rect.colliderect(two.rect)
    # it checks for collision and returns collision

def collide_with_walls(sprite, group, dir):
     #checks sprite collision
     if dir == 'x':
        #checks collision on x axis
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
            #the first hit that we hit
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2
                #moves the sprite backwards based on the collision
            if hits[0].rect.centerx<sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right+sprite.hit_rect.width/2
            #moves the sprite back to the initial position
        sprite.vel.x=0
        #resets the velocity to 0
        sprite.hit_rect.centerx = sprite.pos.x
        
               
         
     if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
            #the first hit that we hit
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2                    
            if hits[0].rect.centery<sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom +sprite.hit_rect.height/2    
                #moves the player back to the position so it does not go through the wall        
            sprite.vel.y=0
            # sets velocity back to 0
            sprite.hit_rect.centery = sprite.pos.y

def bounce_with_walls(sprite, group, dir):
     #checks sprite collision
     if dir == 'x':
        #checks collision on x axis
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            sprite.vel.x *= -1
            #makes the sprite reverse direction when touching a wall
        sprite.hit_rect.centerx = sprite.pos.x
        
               
         
     if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            sprite.vel.y *= -1
            #also makes the sprite direction reverse when touching a wall
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
        #prints the initial position
        if self.vel.x != 0  and self.vel.y != 0:
            self.vel *=0.7071
        #slows down the player when walking diagonally
        self.image.set_colorkey((255,255,255))
        #removes the white in the image
        self.coins = 0
        self.last_mine = 0

    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            #how often it updates in milliseconds
            self.last_update = now
            #sets the last update time to reset the animation timer
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            # sets the current frame to the next one
            bottom = self.rect.bottom
            # sets the bottom of the image to the bottom
            self.image = self.idle_frames[self.current_frame]
            # sets the image to the curreent frame
            self.rect = self.image.get_rect()
            # sets the imange
            self.rect.bottom = bottom
            
        self.image.set_colorkey((255,255,255))
    def mining(self):
        #uses time element to get now
        now = pg.time.get_ticks()
        hits = pg.sprite.spritecollideq(self,self.game.all_ores, False)
        if hits:
            self.last_mine=now
        if now - self.last_mine >= 2000:
            pg.spritecollide
                 
             
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE*2,0,TILESIZE,TILESIZE),
                            self.spritesheet.get_image(TILESIZE*3,0,TILESIZE,TILESIZE),]
        #sets where each of the frames for the animation are
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
        #slows down the sprite so it travels at the same speed while travelling diagonally
        #change velocity based on which key is pressed
    def update(self):
        hits =  pg.sprite.spritecollide(self, self.game.all_collectables, True)
        if hits:
             for i in range (10):
                 Particle(self.game, hits[0].pos.x, hits[0].pos.y)
             self.coins += 1
             self.game.pickup_snd.play()
        self.get_keys()
        #gets the keys so we can collect inputs
        self.animate()
        self.rect.center=self.pos
        #sets the position
        self.pos += self.vel * self.game.dt
        #moves the position in accordance to the velocity and tick rate
        self.hit_rect.centerx=self.pos.x
        #sets the position of x again
        collide_with_walls(self, self.game.all_walls, 'x')
        collide_with_walls(self, self.game.all_ores, 'x')
        # checks if the player is against a wall
        self.hit_rect.centery = self.pos.y
        #sets the y position
        collide_with_walls(self, self.game.all_walls, 'y')
        collide_with_walls(self, self.game.all_ores, 'y')
        #schecks if the player is touching a wall
        self.rect.center = self.hit_rect.center
    
        #sets where each of the frames for the animation are



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
                self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
                self.load_images()
                self.image = self.spritesheet.get_image(0,TILESIZE*2, TILESIZE, TILESIZE)
                #makes the color white
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.x = x*TILESIZE
                self.y = y*TILESIZE
                self.rect.x = self.x
                self.rect.y = self.y
                self.image.set_colorkey((255,255,255))
                #removes the white in the image                
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
        def load_images(self):
                self.idle_frames = [self.spritesheet.get_image(0,TILESIZE*2,TILESIZE, TILESIZE)]

class Particle(Sprite):
        
        def __init__(self, game, x, y):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_particles
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE/8,TILESIZE/8))
                # sets the image size to the size of the time
                self.image.fill(GREEN)
                #makes the color white
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.pos = vec(x,y)
                self.speed = 25
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                self.countdown = Cooldown(5000)
                self.countdown.eventtime=floor(pg.time.get_ticks()/1000)
                self.image.set_colorkey((255,255,255))
                #removes the white in the image                
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                print('particle initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
                
        def update(self):
             self.countdown.ticking()
             self.pos.x +=self.speed*randint(-5,5)
             self.pos.y += self.speed*randint(-5,5)
             print("'updaiting")
             if self.countdown.delta > 10:
                  self.kill()
             self.rect.x = self.pos.x
             self.rect.y = self.pos.y

class Ores(Sprite):
        
        def __init__(self, game, x, y, ore):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_ores
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE,TILESIZE))
                # sets the image size to the size of the time
                self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
                self.load_images(ore)
                #makes the color white
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.x = x*TILESIZE
                self.y = y*TILESIZE
                self.rect.x = self.x
                self.rect.y = self.y
                self.image.set_colorkey((255,255,255))
                #removes the white in the image                
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
        def load_images(self, ore):
            if ore == 'iron':
                self.idle_frames = [self.spritesheet.get_image(TILESIZE,TILESIZE*2,TILESIZE, TILESIZE)]
                
                self.image = self.spritesheet.get_image(TILESIZE,TILESIZE*2, TILESIZE, TILESIZE)

class Mob(Sprite):
        def __init__(self, game, x, y):
            #init runs only once at the start
            self.groups = game.all_sprites, game.all_mobs
            # gets game class into this code
            Sprite.__init__(self, self.groups)
            self.game = game
            # sets the game = to game
            self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
            #adds the spritesheet
            self.load_images()
            #allows the animations to load
            self.image = pg.Surface((TILESIZE,TILESIZE))
            #sets the image of the player
            self.image = self.spritesheet.get_image(0,TILESIZE, TILESIZE, TILESIZE)
            #sets the image of the player
            self.rect = self.image.get_rect()
            #sets the shape to a rectangle
            
            self.hit_rect =  MOB_HIT_RECT
            self.vel = vec(ENEMY_SPEED,ENEMY_SPEED)
            self.pos = vec(x*TILESIZE,y*TILESIZE)
            # sets the size fo the pixel, the color, and the position and velocity
            #sets some animation things
            self.last_update = 0
            self.current_frame = 0
            #sets some animation things
            print('mob initialized...')
            print(self.rect.x)
            print(self.rect.y)
            # prints initialization informations
        def animate(self):
            # use the time element to get now
            now = pg.time.get_ticks()
            if now - self.last_update > 100:
                #how often it updates in milliseconds
                self.last_update = now
                #sets the last update time to reset the animation timer
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                # sets the current frame to the next one
                bottom = self.rect.bottom
                # sets the bottom of the image to the bottom
                self.image = self.idle_frames[self.current_frame]
                # sets the image to the curreent frame
                self.rect = self.image.get_rect()
                # sets the imange
                self.rect.bottom = bottom
                
            self.image.set_colorkey((255,255,255))
        def load_images(self):
            self.idle_frames = [self.spritesheet.get_image(0,TILESIZE,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE,TILESIZE,TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE*2,TILESIZE,TILESIZE,TILESIZE),
                                self.spritesheet.get_image(TILESIZE*3,TILESIZE,TILESIZE,TILESIZE),]
        def chase(self, obj): 
            self.posxdiff = obj.pos.x - self.pos.x

            self.posydiff = obj.pos.y - self.pos.y
            self.posdiff = (self.posxdiff**2 + self.posydiff**2)**(1/2)
            if self.pos.x != obj.pos.x:
                self.vel.x = ENEMY_SPEED*self.posxdiff/self.posdiff
            else:
                self.vel.x = 0

            if self.pos.y != obj.pos.y:
                self.vel.y = ENEMY_SPEED*self.posydiff/self.posdiff
            else:
                self.vel.y = 0
            
        def update(self):

            # if (self.pos.x >= WIDTH-TILESIZE):
            #     print ('crossing +x border')
            #     self.vel.x *= -1
            
            # if (self.pos.x <= 0):
            #     print ('crossing -x border')
            #     self.vel.x*=-1

            # if (self.pos.y >= HEIGHT-TILESIZE):
            #     print ('crossing -y border')
            #     self.vel.y*=-1
                
            # if (self.pos.y <= 0):
            #     print ('crossing +y border')
            #     self.vel.y*=-1
            #checks if the mob is leaving the screen


            self.animate()
            self.chase(self.game.player)
            self.rect.center=self.pos
            #sets the position
            self.pos = self.pos + (self.vel * self.game.dt)
            #changes the 
            self.hit_rect.centerx=self.pos.x
            collide_with_walls(self, self.game.all_walls, 'x')
            collide_with_walls(self, self.game.all_ores, 'x')
            # checks if the player is against a wall
            self.hit_rect.centery = self.pos.y
            #sets the y position
            collide_with_walls(self, self.game.all_walls, 'y')
            collide_with_walls(self, self.game.all_ores, 'y')
            self.rect.center = self.hit_rect.center
            # makes the collison with walls on the y axis 
class Collectable(Sprite):  
        def __init__(self, game, x, y, collectable):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_collectables
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE,TILESIZE))
                # sets the image size to the size of the time
                self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
                self.load_images(collectable)
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.pos = vec(x*TILESIZE,y*TILESIZE)
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                self.image.set_colorkey((255,255,255))
                #removes the white in the image                
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
        def load_images(self, collectable):
            if collectable == 'battery':
                self.idle_frames = [self.spritesheet.get_image(0,TILESIZE*3,TILESIZE, TILESIZE)]
                self.image = self.spritesheet.get_image(0,TILESIZE*3, TILESIZE, TILESIZE)
                #makes the color white
                self.rect = self.image.get_rect()
