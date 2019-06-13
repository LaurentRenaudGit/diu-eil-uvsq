# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 13:48:29 2019

@author: laure
"""
import sys, pygame, random
pygame.init()

SIZE = [1200, 800]
width, height = SIZE
WHITE = [255, 255, 255]
BLACK = [  0,   0,   0]
RED   = [255,   0,   0]

screen = pygame.display.set_mode(SIZE)

class Voyageur:
    def __init__(self,surface,position,taille,vitesse,couleur1):
        self.surface = surface
        self.position = position
        self.taille = taille
        self.vitesse = vitesse
        self.couleur1 = couleur1
    
    # affichage du voyageur
    def display(self):
        pygame.draw.circle(self.surface,self.couleur1,self.position,self.taille[0],self.taille[1])
        pygame.display.flip()

    # observation de l'environnement du voyageur
    def scan(self):
        pass

    # mouvement du voyageur    
    def move(self):
        self.position[0] = self.position[0] + self.vitesse[0]
        self.position[1] = self.position[1] + self.vitesse[1]
    
    def bounce(self):
        if ((self.position[0] > (width - self.taille[0]/2)) or (self.position[0] < self.taille[0]/2)):
            self.vitesse[0] = - self.vitesse[1]
        if ((self.position[1] > (height - self.taille[0]/2)) or (self.position[1] < self.taille[0]/2)):
            self.vitesse[1] = - self.vitesse[1]

# création de la liste des voyageurs
liste_voyageurs = []                        
for i in range(10):
    #temp_xVel = int(random.randint(1,10)) + 1
    temp_xVel = 2
    #temp_yVel = int(random.randint(1,10)) + 1
    temp_yVel = -3
    temp_position = [50+random.randint(1,1100),50+random.randint(1,700)]
    temp_vitesse = [2,-3]
    liste_voyageurs.append(Voyageur(screen,temp_position,(50,5),temp_vitesse,RED))

    
#    background(0,0,0)
    
done = False
clock = pygame.time.Clock()
 
while not done:
 
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
     
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
    
    for individu in liste_voyageurs:
        #ball.scan()
        individu.move()
        individu.display()

    #screen.fill(black)
    pygame.time.wait(10)
    
pygame.quit()