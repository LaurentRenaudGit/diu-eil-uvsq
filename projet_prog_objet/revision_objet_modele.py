# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 08:44:43 2019

@author: laure
"""
import string, random

class Sommet():
    """ represente un sommet du graphe """
    def __init__(self,nom = None):
        self.nom = nom

class Arc():
    """ represente un arc du graphe """
    def __init__(self, debut, fin):
        assert isinstance(debut,Sommet)
        assert isinstance(fin,Sommet)
        self.debut = debut
        self.fin = fin
    
    def __str__(self):
        return "Arc de début "+str(self.debut)+" et de fin "+str(self.fin)
    
    def getDebut(self):
        return self.debut

    def getFin(self):
        return self.fin


class Graphe():
    """ represente un graphe """
    def __init__(self, nom = None):
        self.nom = nom
        self.sommets = []
        self.arcs = []
    
    def ajouterSommet(self,nom_sommet):
        s = Sommet(nom_sommet)
        self.sommets.append(s)
    
    def ajouterArc(self,debut_arc,fin_arc):
        a = Arc(debut_arc, fin_arc)
        self.arcs.append(a)
    
    def afficheSommets(self):
        for s in self.sommets:
            print(str(s.nom))
            
    def afficheArcs(self):
        for a in self.arcs:
            debut_arc = a.getDebut()
            fin_arc = a.getFin()
            print(str(debut_arc.nom)+" --> "+str(fin_arc.nom))
    
    def degreSortant(self,sommet):
        return len([arc for arc in self.arcs if arc.getDebut() == sommet])
    
    def afficheTousdegressortants(self):
        for s in self.sommets:            
            print("Le sommet "+str(s.nom)+" possède "+str(
                        self.degreSortant(s))+" arc(s) sortant(s).")
            


g1 = Graphe("Mon graphe")
alphabet = list(string.ascii_uppercase)

for lettre in alphabet:
    g1.ajouterSommet(lettre)

for i in range(100):
    index_debut = random.randint(0,25)
    index_fin   = random.randint(0,25)
    g1.ajouterArc(g1.sommets[index_debut],g1.sommets[index_fin])

#g1.afficheSommets()
g1.afficheArcs()
g1.afficheTousdegressortants()
