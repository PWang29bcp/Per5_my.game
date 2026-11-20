# sprites are graphic entities in a game
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
import random as r

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
        self.groups = game.all_sprites, game.all_players
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
        self.acl = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        # sets the size fo the pixel, the color, and the position and velocity and acceleration
        self.last_update = 0
        self.current_frame = 0
        self.mines = 0
        #sets up some important variables things
        print('player initialized...')
        print(self.rect.x)
        print(self.rect.y)
        #prints the initial position
       
        #slows down the player when walking diagonally
        self.image.set_colorkey((255,255,255))
        #removes the white in the image
        self.coins = 0
        self.last_mine = 0
        self.ores=0
        self.miningprogress = 0
        self.transporting = False
        #more important variables

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
        mines = pg.sprite.spritecollide(self, self.game.all_ores, False)
        now = pg.time.get_ticks()
        # checks for collision and current time
        if mines:
             print('trying to mine')
             self.miningprogress = now - self.mines
            # makes sure the program is running and calculates time of mining
             
             if self.miningprogress > 1000:
                
                print('trying to mine')
                pg.sprite.spritecollide(self, self.game.all_ores, True)
                self.ores += 1
                # kills the ore and adds one to the count after time

        else:
             self.mines=now
             #resets mining timer
    def newroom(self):
        transport = pg.sprite.spritecollide(self, self.game.all_gateways, False)
        # checks if player is crossing a transport barrier
        if transport:
             print('transporting....')   
             self.transporting = True
        else:
             self.transporting = False         
            #determins if the player is getting transported
                 
             
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE*2,0,TILESIZE,TILESIZE),
                            self.spritesheet.get_image(TILESIZE*3,0,TILESIZE,TILESIZE),]
        #sets where each of the frames for the animation are
    def get_keys(self):
        
        #listen for events specific to keys
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
          
            self.acl.x=-PLAYER_SPEED
            #allows for the player to go left using the a or left keys

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            
            self.acl.x=PLAYER_SPEED
            #allows the player to go right using the right or d keys

        if keys[pg.K_UP] or keys[pg.K_w]:
            
            self.acl.y=-PLAYER_SPEED

            #allows the palyer to go up using the w or up keys, it is reverse for some reason

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            
            self.acl.y=PLAYER_SPEED
            #allows the player to go down using the down or s key, is also reverse
        if keys[pg.K_p]:
            print('')
            self.game.mob.explode()
        if keys[pg.K_0]:
            Mob(self.game , self.pos.x, self.pos.y)
        # some testing keys
        #change acceleration based on which key is pressed
    def get_aggrod(self):
        aggroing = pg.sprite.collide_circle(self, self.game.aggro)
        # checks for collision wiht the aggro range of the mob
        if aggroing:

            print('trying to agrro')
    
    def update(self):
        self.acl = vec (0,0)
        #sets acceleration to 0
        collect =  pg.sprite.spritecollide(self, self.game.all_collectables, True)
        #checks for collision with coins
        if collect:
             for i in range (100):
                 Particle(self.game, collect[0].pos.x, collect[0].pos.y, GREEN)
             self.coins += 1
             self.game.pickup_snd.play()
             #summons particles when the coins are collected
        self.mining()
        self.newroom()
        self.get_keys()
        #runs a bunch of programs
        self.acl.x += self.vel.x*PLAYER_FRIC
        self.acl.y += self.vel.y*PLAYER_FRIC
        #accounts for friction
        self.vel.x += self.acl.x
        self.vel.y += self.acl.y
        #changes the velocity based on the acceleration
        
        # if self.vel.x >= PLAYER_MAX_SPEED:
        #     self.vel.x = PLAYER_MAX_SPEED
        #     print('trying to cap speed')
        # if self.vel.y >= PLAYER_MAX_SPEED:
        #     self.vel.y = PLAYER_MAX_SPEED
        #speed cap for player
        
        
        self.animate()
        #animates the player
        self.rect.center=self.pos
        #sets the position

        self.pos.x+= self.vel.x + 0.5 *self.acl.x
        self.pos.y+= self.vel.y + 0.5 *self.acl.y
        #moves the position in accordance to the velocity and acceleration
        self.hit_rect.centerx=self.pos.x
        #sets the position of x 
        
        collide_with_walls(self, self.game.all_walls, 'x')
        # checks if the player is against a wall
        self.hit_rect.centery = self.pos.y
        #sets the y position
        collide_with_walls(self, self.game.all_walls, 'y')
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
                #makes the image the spritesheet
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.x = x*TILESIZE
                self.y = y*TILESIZE
                self.rect.x = self.x
                self.rect.y = self.y
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                self.image.set_colorkey((255,255,255))
                #removes the white in the image             
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
        def load_images(self):
                self.idle_frames = [self.spritesheet.get_image(0,TILESIZE*2,TILESIZE, TILESIZE)]
                # loads the sprite info
        
class Spiketrap(Sprite):
        pass
        # def __init__(self, game, x, y):
        #         #init runs only once at the start
        #         self.groups = game.all_sprites, game.all_traps
        #         # gets game class into this code
        #         Sprite.__init__(self, self.groups)
        #         self.game = game
        #         # sets the game = to game
        #         self.image = pg.Surface((TILESIZE,TILESIZE))
        #         # sets the image size to the size of the time
        #         self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        #         self.load_images()
        #         self.image = self.spritesheet.get_image(0,TILESIZE*2, TILESIZE, TILESIZE)
        #         #makes the color white
        #         self.rect = self.image.get_rect()
        #         #sets the shape to a rectangle
        #         self.vx, self.vy = 0,0
        #         self.x = x*TILESIZE
        #         self.y = y*TILESIZE
        #         self.rect.x = self.x
        #         self.rect.y = self.y
        #         self.image.set_colorkey((255,255,255))
        #         #removes the white in the image                
        #         #sets the x and y values
        #         # sets the size fo the pixel, the color, and the position and velocity
        #         print('wall initialized...')
        #         print(self.rect.x)
        #         print(self.rect.y)
        #         #prints initialization information
        # def load_images(self):
        #         self.idle_frames = [self.spritesheet.get_image(0,TILESIZE*2,TILESIZE, TILESIZE)]
        
class Gateway(Sprite):
        
        def __init__(self, game, x, y):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_gateways
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE,TILESIZE))
                # sets the image size to the size of the time
                self.image.fill(GREEN)
                #makes the color green
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.x = x*TILESIZE
                self.y = y*TILESIZE
                self.rect.x = self.x
                self.rect.y = self.y
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                self.image.set_colorkey((255,255,255))
                #removes the white in the image                
                
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
        

class Particle(Sprite):
        
        def __init__(self, game, x, y, color):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_particles
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE/8,TILESIZE/8))
                # sets the image size
                self.image.fill(color)
                #makes the color based on the color inputted
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx = r.randint(-100,100)
                self.vy = ((100)**2-(self.vx)**2)**(1/2)
                self.slowdown = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
                self.posorneg =[-1,1]
                self.vy *= r.choice(self.slowdown)
                self.vx *= r.choice(self.slowdown)
                self.vy *= r.choice(self.posorneg)
                self.pos = vec(x,y)
                self.speed = 1
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                self.countdown = Cooldown()
                self.countdown.eventtime=floor(pg.time.get_ticks()/1000)
                # makes the particles explode in a circle and them make them more random
                print('particle initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
                
        def update(self):
             self.countdown.ticking()
             self.pos.x +=self.speed*self.vx*self.game.dt
             self.pos.y += self.speed*self.vy*self.game.dt
             if self.countdown.delta > 2:
                  self.kill()
             self.rect.x = self.pos.x
             self.rect.y = self.pos.y
             #makes it so that particles die after a little bit



class Ores(Sprite):
        
        def __init__(self, game, x, y, ore):
                #init runs only once at the start
                self.groups = game.all_sprites, game.all_ores
                # gets game class into this code
                Sprite.__init__(self, self.groups)
                self.game = game
                # sets the game = to game
                self.image = pg.Surface((TILESIZE,TILESIZE))
                # sets the image size to the size of the tile
                self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
                self.load_images(ore)
                #makes the image based on the ore
                self.rect = self.image.get_rect()
                #sets the shape to a rectangle
                self.vx, self.vy = 0,0
                self.x = x*TILESIZE
                self.y = y*TILESIZE
                self.rect.x = self.x
                self.rect.y = self.y
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                self.image.set_colorkey((255,255,255))
                #removes the white in the image                
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
        def load_images(self, ore):
            if ore == 'iron':
                self.idle_frames = [self.spritesheet.get_image(TILESIZE,TILESIZE*2,TILESIZE, TILESIZE)]
                
                self.unmined = self.spritesheet.get_image(TILESIZE,TILESIZE*2, TILESIZE, TILESIZE)
                self.image = self.spritesheet.get_image(TILESIZE,TILESIZE*2, TILESIZE, TILESIZE)
                self.mining1 = self.spritesheet.get_image(TILESIZE*2,TILESIZE*2, TILESIZE, TILESIZE)
                self.mining2 = self.spritesheet.get_image(TILESIZE*3,TILESIZE*2, TILESIZE, TILESIZE)
                #loads images for iron ore
        def update(self):
            mining = pg.sprite.spritecollide(self, self.game.all_players, False)
            #checks again if player is in contact
            if mining:

                if self.game.player.miningprogress < 333:
                    self.image = self.unmined  
                elif self.game.player.miningprogress < 666:
                    self.image = self.mining1
                elif self.game.player.miningprogress > 666:
                    self.image = self.mining2
                #changes image based on mining progress
                
            else:
                self.image = self.unmined
                #changes image back if player leaves
            

class Mob(Sprite):
        def __init__(self, game, x, y):
            print (x, y)
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
            #sets the image size
            self.image = self.spritesheet.get_image(0,TILESIZE, TILESIZE, TILESIZE)
            #sets the image of the player
            self.rect = self.image.get_rect()
            #sets the shape to a rectangle
            self.hit_rect =  MOB_HIT_RECT
            self.vel = vec(0,0)
            self.acl = vec(0,0)
            self.pos = vec(x*TILESIZE,y*TILESIZE)
            # sets the size fo the pixel, the color, and the position and velocity and acceleration
            self.last_update = 0
            self.current_frame = 0
            self.dying = 0
            self.exploding = False
            #sets some imporant variables
            print(self.pos)
            print('mob initialized...')
            print(self.rect.x)
            print(self.rect.y)
            # prints initialization informations
            self.image.set_colorkey((255,255,255))
            #removes white from image
        def aggroing(self, obj):
            self.posxdiff = obj.pos.x - self.pos.x
            self.posydiff = obj.pos.y - self.pos.y
            self.posdiff = (self.posxdiff**2 + self.posydiff**2)**(1/2)
            if self.posdiff < TILESIZE*5:
                 print ('trying to chase')
                 self.chase(obj)
            else:
                self.acl = vec(0,0)
            #checks the distance between the player and the mob, if it is close enough the mob aggros
                 
        
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
            self.death_frame = self.spritesheet.get_image(TILESIZE*4,TILESIZE,TILESIZE, TILESIZE)
            #loads all the images
        def chase(self, obj): 
            
            if self.pos.x != obj.pos.x:
                self.acl.x = ENEMY_SPEED*self.posxdiff/self.posdiff
            else:
                self.vel.x = 0

            if self.pos.y != obj.pos.y:
                self.acl.y = ENEMY_SPEED*self.posydiff/self.posdiff
            else:
                self.vel.y = 0
            #makes the mob chase smoothly
        def explode(self):
            self.image = self.death_frame
            self.now = pg.time.get_ticks()
            self.dying = self.now
            self.exploding = True
            self.image.set_colorkey((255,255,255))
            #instantiates the death animation
            

            

        def update(self):
            if self.exploding == True:
                self.now = pg.time.get_ticks()
                self.dyingtime = self.now-self.dying
                if self.dyingtime>1000: 
                    print('im dying!!!!')
                    self.kill()
                # makes sure the mob dies after some amount of seconds
                for i in range (10): 
                    self.explodycolors = ['RED','ORANGE','YELLOW']
                    self.color = r.choice(self.explodycolors)
                    Particle(self.game, self.pos.x, self.pos.y, self.color)
                    #makes particles when the mob dies
                # also makes sure almost all other programs stop running
                
                    

                    
            else:
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
                self.acl = vec(0,0)

                self.animate()
                self.aggroing(self.game.player)
                #sets the position
                self.acl.x += self.vel.x*MOB_FRIC
                self.acl.y += self.vel.y*MOB_FRIC

                self.vel.x += self.acl.x
                self.vel.y += self.acl.y
                #sets acceleration, friction, and its effect on velocity

                
            self.rect.center=self.pos
            
            self.pos += self.vel + 0.5*self.acl
            #changes the pos based on acl
            
            self.hit_rect.centerx=self.pos.x
            collide_with_walls(self, self.game.all_walls, 'x')
            collide_with_walls(self, self.game.all_ores, 'x')
            # checks if the mob is against a wall
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
                # sets the image size to the size of the tile
                self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
                self.load_images(collectable)
                #sets the image to the sprite image
                self.vx, self.vy = 0,0
                self.pos = vec(x*TILESIZE,y*TILESIZE)
                self.rect.x = self.pos.x
                self.rect.y = self.pos.y
                
                #sets the x and y values
                # sets the size fo the pixel, the color, and the position and velocity
                self.image.set_colorkey((255,255,255))
                #removes the white in the image                
                print('wall initialized...')
                print(self.rect.x)
                print(self.rect.y)
                #prints initialization information
        def load_images(self, collectable):
            if collectable == 'battery':
                self.idle_frames = [self.spritesheet.get_image(0,TILESIZE*3,TILESIZE, TILESIZE)]
                self.image = self.spritesheet.get_image(0,TILESIZE*3, TILESIZE, TILESIZE)
                self.rect = self.image.get_rect()
                # loads the images for the sprite
class Aggrorange(Sprite):
    def __init__(self, game, x, y, radius, enemy):
        self.groups = game.all_sprites, game.all_aggros
        #puts the sprite in groups
        print(x, y)
        Sprite.__init__(self, self.groups)
        self.game = game
        self.enemy = enemy
        self.radius = radius
        #transfers stuff to attributes
        self.image = pg.Surface((TILESIZE*10, TILESIZE*10))
        self.image.set_colorkey(BLACK)
        # sets the image to be remove black
        self.rect = self.image.get_rect()
        # makes the rectangle
        self.vel = vec(0,0) 
        self.pos = vec(x,y) * TILESIZE
        #sets pos and velocity
        self.rect.center = self.pos
        pg.draw.circle(self.image, CYAN, (TILESIZE*5, TILESIZE*5), TILESIZE*5)
        pg.draw.circle(self.image, BLACK, (TILESIZE*5, TILESIZE*5), TILESIZE*5-1)
        # makes the cyan circle only exist, as black covers it and then is removed
        print (self.pos)

        
        print('aggro initialized')

    def update(self):
        self.pos = self.enemy.pos
        self.rect.center = self.pos
        pg.draw.circle(self.image, CYAN, (TILESIZE*5, TILESIZE*5), TILESIZE*5)
        pg.draw.circle(self.image, BLACK, (TILESIZE*5, TILESIZE*5), TILESIZE*5-1)
        # draws the circle again
        if self.enemy.exploding == True:
            self.kill()
            #kills it along with the sprite





class LoadingScreen(Sprite):
     pass