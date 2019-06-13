# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:25:36 2019

@author: laure
"""

class Sommet:
    """stocke un sommet du graphe"""
    
    def __init__(self,nom = None):
        self.nom = nom
    
    def __str__(self):
        return self.nom

class Arc:
    """represente un arc du graphe"""
    
    def __init__(self,pdebut, pfin):
        """pdebut et pfin sont des objets Sommet"""
        assert isinstance(pdebut, Sommet)
        self.extremites = [pdebut, pfin]
    
    def __str__(self):
        return "arc de début " + str(self.extremites[0].nom) + " et de fin " + str(self.extremites[1].nom)
    
    def getDebut(self):
        return self.extremites[0]
    
    def setFin(self, nouvelle_fin):
        self.extremites[1] = nouvelle_fin
        
class Graphe:
    """stocke un graphe orienté"""
    
    def __init__(self, nom = None):
        self.nom = nom
        self.sommets = []
        self.arcs = []
    
    def ajouterSommet(self, nom_du_sommet):
        """crée et ajoute un sommet au graphe"""
        s = Sommet(nom_du_sommet)
        self.sommets.append(s)
    
    def ajouterArc(self, debut, fin):
        self.arcs.append(Arc(debut,fin))
        
    def degreSortant(self, sommet):
        compteur = 0
        for arc in self.arcs:
            if arc.getDebut() == sommet:
                compteur += 1
        return compteur
        return len([arc for arc in self.Arcs if arc.getDebut() == sommet ])
        
        
g = Graphe()
g.ajouterSommet("titi")
print(g.degreSortant("titi"))