#!c:\python25

import pygame, os
from pygame.locals import *

class Box():
  def __init__(self, type_of_block):
    self.counter = 0
    self.going_down = True
    self.state = 1

    if(type_of_block == 1): #O
      self.image = pygame.image.load(os.path.join('pix', 'yellowblock.gif')).convert()
      self.starting_pos = [Rect(65,5,15,15), Rect(80,5,15,15), Rect(65,-10,15,15), Rect(80,-10,15,15)]
      self.display_pos = [Rect(215,95,15,15), Rect(230,95,15,15), Rect(215,110,15,15), Rect(230,110,15,15)]
      self.type = 'O'
    if(type_of_block == 2): #I
      self.image = pygame.image.load(os.path.join('pix', 'turqblock.gif')).convert()
      self.starting_pos = [Rect(50,-10,15,15), Rect(65,-10,15,15), Rect(80,-10,15,15), Rect(95,-10,15,15)]
      self.display_pos = [Rect(200,95,15,15), Rect(215,95,15,15), Rect(230,95,15,15), Rect(245,95,15,15)]
      self.type = 'I'
    if(type_of_block == 3): #L
      self.image = pygame.image.load(os.path.join('pix', 'blueblock.gif')).convert()
      self.starting_pos = [Rect(50,-10,15,15), Rect(65,-10,15,15), Rect(80,-10,15,15), Rect(80,5,15,15)]
      self.display_pos = [Rect(215,95,15,15), Rect(230,95,15,15), Rect(245,95,15,15), Rect(245,110,15,15)]
      self.type = 'L'
    if(type_of_block == 4): #J
      self.image = pygame.image.load(os.path.join('pix', 'orangeblock.gif')).convert()
      self.starting_pos = [Rect(50,5,15,15), Rect(50,-10,15,15), Rect(65,-10,15,15), Rect(80,-10,15,15)]
      self.display_pos = [Rect (215,110,15,15), Rect(215,95,15,15), Rect(230,95,15,15), Rect(245,95,15,15)]
      self.type = 'J'
    if(type_of_block == 5): #S
      self.image = pygame.image.load(os.path.join('pix', 'redblock.gif')).convert()
      self.starting_pos = [Rect(95,-10,15,15), Rect(80,-10,15,15), Rect(80,5,15,15), Rect(65,5,15,15)]
      self.display_pos = [Rect(245,95,15,15), Rect(230,95,15,15), Rect(230,110,15,15), Rect(215,110,15,15)]
      self.type = 'S'
    if(type_of_block == 6): #Z
      self.image = pygame.image.load(os.path.join('pix', 'greenblock.gif')).convert()
      self.starting_pos = [Rect(65,-10,15,15), Rect(80,-10,15,15), Rect(80,5,15,15), Rect(95,5,15,15)]
      self.display_pos = [Rect(215,95,15,15), Rect(230,95,15,15), Rect(230,110,15,15), Rect(245,110,15,15)]
      self.type = 'Z'
    if(type_of_block == 7): #T 
      self.image = pygame.image.load(os.path.join('pix', 'purpleblock.gif')).convert()
      self.starting_pos = [Rect(80,-10,15,15), Rect(65,5,15,15), Rect(80,5,15,15), Rect(95,5,15,15)]
      self.display_pos = [Rect(230,95,15,15), Rect(215,110,15,15), Rect(230,110,15,15), Rect(245,110,15,15)]
      self.type = 'T'
  
  def update(self, time_passed, grid, speed):
    for pos in self.starting_pos:
      if(pos.bottom == 305):
        self.going_down = False
      for i in grid:
        for ii in i.starting_pos:
          if(pos.bottom == ii.top and pos.right == ii.right and pos.left == ii.left):
            self.going_down = False
    if self.counter < time_passed:
      self.counter = time_passed + speed
      for pos in self.starting_pos:
        pos.top += 15
        
  def move_right(self, grid):
    for pos in self.starting_pos:
      if(pos.right == 155):
        return
      for i in grid:
        for ii in i.starting_pos:
          if(pos.right == ii.left and pos.top == ii.top):
            return      
    for pos in self.starting_pos:
      pos.right +=15
        
  def move_left(self, grid):
    for pos in self.starting_pos:
      if(pos.left == 5):
        return
      for i in grid:
        for ii in i.starting_pos:
          if(pos.left == ii.right and pos.top == ii.top):
            return          
    for pos in self.starting_pos:
      pos.right -=15
  
  def rotate(self):
    old_pos = self.starting_pos[:]
    if(self.type == 'I'):
      if(self.state == 1):
        self.starting_pos[0] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-30, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left, self.starting_pos[2].top+15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 2
        return
      if(self.state == 2):
        self.starting_pos[0] = Rect(self.starting_pos[2].left-30, self.starting_pos[2].top, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left-15, self.starting_pos[2].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left+15, self.starting_pos[2].top, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 1
        return
    if(self.type == 'L'):
      if(self.state == 1):
        self.starting_pos[0] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-30, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left+15, self.starting_pos[2].top, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 2
        return              
      if(self.state == 2):
        self.starting_pos[0] = Rect(self.starting_pos[2].left+30, self.starting_pos[2].top, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left+15, self.starting_pos[2].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left, self.starting_pos[2].top+15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return        
        self.state = 3
        return
      if(self.state == 3):
        self.starting_pos[0] = Rect(self.starting_pos[2].left, self.starting_pos[2].top+30, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left, self.starting_pos[2].top+15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left-15, self.starting_pos[2].top, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return        
        self.state = 4
        return            
      if(self.state == 4):
        self.starting_pos[0] = Rect(self.starting_pos[2].left-30, self.starting_pos[2].top, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left-15, self.starting_pos[2].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return        
        self.state = 1
    if(self.type == 'J'):
      if(self.state == 1):
        self.starting_pos[0] = Rect(self.starting_pos[1].left+15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left, self.starting_pos[1].top+15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left, self.starting_pos[1].top+30, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 2
        return              
      if(self.state == 2):
        self.starting_pos[0] = Rect(self.starting_pos[1].left, self.starting_pos[1].top+15, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left-15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left-30, self.starting_pos[1].top, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 3
        return
      if(self.state == 3):
        self.starting_pos[0] = Rect(self.starting_pos[1].left-15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left, self.starting_pos[1].top-15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left, self.starting_pos[1].top-30, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 4
        return            
      if(self.state == 4):
        self.starting_pos[0] = Rect(self.starting_pos[1].left, self.starting_pos[1].top-15, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left+15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left+30, self.starting_pos[1].top, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 1
    if(self.type == 'S'):
      if(self.state == 1):
        self.starting_pos[0] = Rect(self.starting_pos[1].left, self.starting_pos[1].top-15, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left+15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left+15, self.starting_pos[1].top+15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 2
        return              
      if(self.state == 2):
        self.starting_pos[0] = Rect(self.starting_pos[1].left+15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left, self.starting_pos[1].top+15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left-15, self.starting_pos[1].top+15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 1
    if(self.type == 'Z'):
      if(self.state == 1):
        self.starting_pos[0] = Rect(self.starting_pos[1].left, self.starting_pos[1].top-15, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left-15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left-15, self.starting_pos[1].top+15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 2
        return              
      if(self.state == 2):
        self.starting_pos[0] = Rect(self.starting_pos[1].left-15, self.starting_pos[1].top, 15, 15)
        self.starting_pos[2] = Rect(self.starting_pos[1].left, self.starting_pos[1].top+15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[1].left+15, self.starting_pos[1].top+15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 1
    if(self.type == 'T'):
      if(self.state == 1):
        self.starting_pos[0] = Rect(self.starting_pos[2].left+15, self.starting_pos[2].top, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left, self.starting_pos[2].top+15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return
        self.state = 2
        return              
      if(self.state == 2):
        self.starting_pos[0] = Rect(self.starting_pos[2].left, self.starting_pos[2].top+15, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left+15, self.starting_pos[2].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left-15, self.starting_pos[2].top, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return        
        self.state = 3
        return
      if(self.state == 3):
        self.starting_pos[0] = Rect(self.starting_pos[2].left-15, self.starting_pos[2].top, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left, self.starting_pos[2].top+15, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-15, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return        
        self.state = 4
        return            
      if(self.state == 4):
        self.starting_pos[0] = Rect(self.starting_pos[2].left, self.starting_pos[2].top-15, 15, 15)
        self.starting_pos[1] = Rect(self.starting_pos[2].left-15, self.starting_pos[2].top, 15, 15)
        self.starting_pos[3] = Rect(self.starting_pos[2].left+15, self.starting_pos[2].top, 15, 15)
        for pos in self.starting_pos:
          if(pos.right > 155 or pos.top < 5 or pos.left < 5):
            self.starting_pos = old_pos[:]
            return        
        self.state = 1                                