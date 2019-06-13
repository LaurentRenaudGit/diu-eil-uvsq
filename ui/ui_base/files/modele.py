#coding: utf-8
import random
import math
import time

class Observable:
    def __init__(self, vue):
        self.observateurs = []

    def attacher_observateur(self, observateur):
        self.observateurs.append(observateur)

    def notifier(self):
        for o in self.observateurs:
            o.mise_a_jour()


class Carre(Observable):
    def __init__(self, x, y, cote, modele):

        Observable.__init__(self,modele.vue)

        self.x = x   #abscisse du centre, entre 0 et 1
        self.y = y   #abscisse de l'ordonnée, entre 0 et 1
        self.cote = cote  #cote du carré, entre 0 et 1


    def mouvement(self, dx, dy):
        self.x += dx
        self.y += dy
        self.notifier()


class Modele:

    def __init__(self, vue):
        self.vue = vue

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
