import pygame, sys
from pygame.locals import *

#A bunch of useful colours
Aqua = (0, 255, 255)
Black = (0,0,0)
Blue = (0,0,255)
Fuchsia = (255,0,255)
Gray = (128,128,128)
Green = (0,128,0)
Lime = (0,255,0)
Maroon = (128,0,0)
NavyBlue = (0,0,128)
Olive = (128,128,0)
Purple = (128,0,128)
Red = (255,0,0)
Silver = (192,192,192)
Teal = (0,128,128)
White = (255,255,255)
Yellow = (255,255,0)

#Main loop
pygame.init()
DISPLAYSURF = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Tower Defence')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()
    Grid = pygame.Rect(10, 20, 200, 300)
