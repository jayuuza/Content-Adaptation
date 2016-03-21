#!c:\python25

import pygame, os
from pygame.locals import *
from sys import exit
from random import *
from box import Box

pygame.init()

screen_size = (315, 310)
game_area = Rect(5, 5, 150, 300)
game_info = Rect(160, 5, 150, 300)
box_display = Rect(185, 65, 100, 70) 
#             gray          white        red       blue       green     black
colours =[(100,100,100),(255,255,255),(255,0,0), (0,255,0), (0,0,255), (0,0,0)]
my_font25 = pygame.font.SysFont(None,25)
my_font20 = pygame.font.SysFont(None,20)
my_font15 = pygame.font.SysFont(None,15)
pygame.display.set_caption('Tetris')
help_text1 = my_font15.render('Tetris:', True, colours[1], colours[0])
help_text2 = my_font15.render('Left and Right keys to move.', True, colours[1], colours[0])
help_text3 = my_font15.render('Up key to rotate blocks.', True, colours[1], colours[0])
start_text = my_font20.render('START', True, colours[1], colours[0])
reset_text = my_font20.render('RESET', True, colours[1], colours[0])
pause_text = my_font20.render('PAUSE', True, colours[1], colours[0])
my_font25.set_bold(True)
game_over = my_font25.render('GAME OVER!', True, colours[1], colours[0])

clock = pygame.time.Clock()
lines = 0
speed = 300
start_flag = 0
start_rect = Rect(165,180,60,30)
reset_rect = Rect(245,180,60,30)

click_sound = pygame.mixer.Sound(os.path.join('sounds', 'click.wav'))
move_sound = pygame.mixer.Sound(os.path.join('sounds', 'move.wav'))
rotate_sound = pygame.mixer.Sound(os.path.join('sounds', 'rotate.wav'))
tetris_sound = pygame.mixer.Sound(os.path.join('sounds', 'tetris.wav'))

screen = pygame.display.set_mode(screen_size, 0, 32)
screen.set_clip(game_info)
screen.fill(colours[0])
screen.blit(help_text1, (165, 250))
screen.blit(help_text2, (165, 265))
screen.blit(help_text3, (165, 280))
pygame.draw.rect(screen, colours[5], start_rect, 0)
pygame.draw.rect(screen, colours[5], reset_rect, 0)
pygame.draw.rect(screen, colours[5], box_display, 2)
screen.blit(start_text, (171, 188))
screen.blit(reset_text, (251, 188))
screen.set_clip(game_area)
screen.fill(colours[0])
pygame.display.update()

grid = [] # a list of all box objects
rects = {290:0, 275:0, 260:0, 245:0, 230:0, 215:0, 200:0, 185:0, 170:0, 155:0, 
         140:0, 125:0, 110:0, 95:0, 80:0, 65:0, 50:0, 35:0, 20:0, 5:0} #dictionary to keep track of the number of box objects on a line

def update():
  screen.set_clip(game_info)
  line_text = my_font25.render('Lines: ' + str(lines), True, colours[1], colours[0] )
  screen.blit(line_text, (165, 10))
  screen.set_clip(game_area)
  for i in grid:
    for pos in i.starting_pos:
      screen.blit(i.image, pos)
  pygame.display.update()

def move_down(key, grid, rects):
  for i in grid:
    for ii in i.starting_pos:
      if(ii.top < key):
        rects[ii.top] -= 1
        ii.top += 15
        rects[ii.top] += 1
  screen.fill(colours[0])
  update()
  pygame.time.wait(30)
  tetris(grid, rects)          

def tetris(grid, rects):
  global lines
  global speed
  sorted_keys = rects.keys()
  sorted_keys.sort(reverse=True)
  for key in sorted_keys:
    if(rects[key] == 10):
      lines += 1
      speed -= 5
      for i in grid:
        for ii in i.starting_pos:
          if ii.top == key:
            pygame.draw.rect(screen, colours[1], ii, 0)
            tetris_sound.play()
            pygame.display.update()
            pygame.time.wait(30)
        i.starting_pos = [ii for ii in i.starting_pos if ii.top != key]
      rects[key] = 0
      grid = [g for g in grid if len(g.starting_pos) > 0]
      move_down(key, grid, rects)

b = Box(randint(1,7))
next_box = Box(randint(1,7))
    
while True:
  pygame.time.wait(1)
  for event in pygame.event.get():
    if event.type == QUIT:
      exit()
    if event.type == MOUSEBUTTONDOWN:
      if pygame.mouse.get_pressed()[0]:
        if start_rect.collidepoint(event.pos):
          click_sound.play()
          start_flag = 1
          screen.set_clip(game_info)
          screen.blit(pause_text, (171, 188))
          pygame.display.update()
        if reset_rect.collidepoint(event.pos):
          click_sound.play()
          start_flag = 0
          screen.set_clip(game_area)
          screen.fill(colours[0])
          screen.set_clip(game_info)
          screen.blit(start_text, (171, 188))
          pygame.display.update()
          lines = 0
          grid = []
          rects = {290:0, 275:0, 260:0, 245:0, 230:0, 215:0, 200:0, 185:0, 170:0, 155:0, 
                     140:0, 125:0, 110:0, 95:0, 80:0, 65:0, 50:0, 35:0, 20:0, 5:0}      

  while start_flag:
    #clock.tick(30)
    pygame.time.wait(1)
    for event in pygame.event.get():
      if event.type == QUIT:
        exit()
      if event.type == KEYDOWN:
        if event.key == K_UP:
          b.rotate()
          rotate_sound.play()
        if event.key == K_LEFT:
          b.move_left(grid)
          move_sound.play()
        if event.key == K_RIGHT:
          b.move_right(grid)
          move_sound.play()
        if event.key == K_DOWN:
          pass
      if event.type == MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0]:
          if start_rect.collidepoint(event.pos):
            click_sound.play()
            if start_flag == 1:
              start_flag = 0
              screen.set_clip(game_info)
              screen.blit(start_text, (171, 188))
            else:
              start_flag = 1
              screen.set_clip(game_info)
              screen.blit(pause_text, (171, 188))
          if reset_rect.collidepoint(event.pos):
            click_sound.play()
            start_flag = 0
            screen.set_clip(game_area)
            screen.fill(colours[0])
            screen.set_clip(game_info)
            screen.blit(start_text, (171, 188))
            pygame.display.update()
            lines = 0
            grid = []
            rects = {290:0, 275:0, 260:0, 245:0, 230:0, 215:0, 200:0, 185:0, 170:0, 155:0, 
                     140:0, 125:0, 110:0, 95:0, 80:0, 65:0, 50:0, 35:0, 20:0, 5:0}
    
    time_passed = pygame.time.get_ticks()
    if(b.going_down):
      screen.set_clip(187, 67, 97, 67)
      screen.fill(colours[0])
      for pos in next_box.display_pos:
        screen.blit(next_box.image, pos)
      b.update(time_passed, grid, speed)
      screen.set_clip(game_area)
      screen.fill(colours[0])
      for pos in b.starting_pos:
        screen.blit(b.image, pos)
    else:
      grid.append(b)
      for pos in b.starting_pos:
        rects[pos.top] += 1
      tetris(grid, rects)    
      b = next_box
      next_box = Box(randint(1,7))
      for i in grid:
        for ii in i.starting_pos:
          if ii.left == 65 and ii.top <= 5:
            start_flag = 0
            screen.blit(game_over, (30, 50))
            pygame.display.update()
    update()