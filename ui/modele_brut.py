#coding: utf-8
import random
import math
import time

class Carre:
    def __init__(self, x, y, cote, modele):


        self.x = x   #abscisse du centre, entre 0 et 1
        self.y = y   #abscisse de l'ordonnée, entre 0 et 1
        self.cote = cote  #cote du carré, entre 0 et 1


    def mouvement(self, dx, dy):
        self.x += dx
        self.y += dy


class Modele:

    def __init__(self):

        #initialisation
        self.liste_carres = []
        nbcarres = 50
        for i in range(nbcarres):
            x = random.random()
            y = random.random()
            cote = random.random()*0.1
            self.liste_carres.append( Carre(x,y, cote, self) )


    def bouge(self):
        for i in range(100):
            for c in self.liste_carres:
                dx = random.randint(-10,10) * 0.001
                dy = random.randint(-10,10) * 0.001
                c.mouvement(dx, dy)
            time.sleep(0.03)
