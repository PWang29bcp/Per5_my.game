import pygame as pg

#general settings
WIDTH = 1024
HEIGHT = 768
TITLE = "placeholder game name"
TILESIZE = 32
FPS = 30

#enemy settings
ENEMY_SPEED = 500

#player settings
PLAYER_SPEED=300
PLAYER_HIT_RECT = pg.Rect(0,0, TILESIZE-5, TILESIZE-5)

#colors
WHITE = (255,255,255)
BGCOLOR = (40,146,155)
PURPLE=(150, 50, 180)#purple backround filler
DGRAY=(74,74,74)#dark grey
GRAY=(140,140,155)#light grey
LGRAY=(198,198,206)#lighter grey
BLUE=(49,66,105)#blue
LBLUE=(73,106,170)#light blue
DBLUE=(41,65,81)# darker blue
BLACK=(0,0,0)#black
BROWN=(139,92,52)#brown
LBROWN=(198,150,57)# light brown
DCYAN=(35,89,98)#dark cyan
LCYAN=(51,187,17)#light cyan
CYAN=(40,146,155)#cyan
TAN=(239,207,139)
GREEN = (0,255,0)
RED = (255,0,0)