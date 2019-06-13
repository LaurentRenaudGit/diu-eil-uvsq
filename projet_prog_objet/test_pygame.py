# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 19:33:43 2019

@author: laure
"""

import sys, pygame, random
pygame.init()

SIZE = [600, 400]
SPEED = [2, 2]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
WHITE = [255, 255, 255]

screen = pygame.display.set_mode(SIZE)

done = False
clock = pygame.time.Clock()
 
while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
 
        # Clear the screen and set the screen background
        screen.fill(WHITE)
        
        pygame.draw.circle(screen,RED,(250,200),100,5)
        pygame.display.flip()

pygame.quit()