#coding: utf-8
import tkinter as tk
import os
from files.modele import *
from functools import partial

class Root(tk.Tk):
    """Hérite de la classe à la base des applications tk"""

    def __init__(self):
        tk.Tk.__init__(self)

        self.largeur = 800 #largeur et hauteur en pixels
        self.title('le titre')

        vue = FenetrePrincipale(self,  self.largeur)
        modele = Modele(vue)
        self.modele = modele
        vue.toile.modele = modele
        vue.toile.initialisation_graphique()


class FenetrePrincipale(tk.Frame):
    """Fenetre principale qui contiendra le menu et la toile (canvas)"""

    def __init__(self, parent, largeur):
        tk.Frame.__init__(self, parent)
        #self.grid()
        self.parent = parent #la root

        self.toile = Toile(largeur, self)
        self.toile.grid(row=0,column=1, sticky = 'E')
        self.focus_set()

        #Menu du dessus
        menubar = tk.Menu(self.parent)
        editmenu = tk.Menu(menubar, tearoff=0)
        trucmenu = tk.Menu(menubar, tearoff=0)

        #editmenu.add_command(label = "Réinitialiser", command = (lambda:self.toile.reset(self)))

        editlabels = ["Charger", "Sauvegarder", "bouger"]

        #lie les items du menu avec la methode menu_appel ci dessous
        for lab in editlabels:
            editmenu.add_command(label = lab, command = (lambda lab = lab:self.menu_appel(lab)))


        self.menubar = menubar
        menubar.add_cascade(label="Édition", menu=editmenu)
        menubar.add_cascade(label="Trucs", menu=trucmenu)

        #montrer le menu
        self.parent.config(menu=menubar)


    def menu_appel(self, event):
        """methode a modifier pour les differents items du menu"""
        if event == "bouger":
            self.parent.modele.bouge()



class Carre_vue:
    """sauvegarde les caractéristiques d'un polygone tkinter"""
    def __init__(self, toile, carre_modele):
        self.observe = carre_modele
        self.toile = toile

        xcentre, ycentre, cote = self.toile.conversion_coord_carre(carre_modele)
        c = cote/2
        x = xcentre
        y = ycentre

        self.x = x
        self.y = y
        self.tk_cle = self.toile.create_polygon(x-c,y-c,x+c,y-c,x+c,y+c,x-c,y+c)
        carre_modele.attacher_observateur(self)

    def mise_a_jour(self):
        new_xc, new_yc, ncote = self.toile.conversion_coord_carre(self.observe)
        self.toile.move(self.tk_cle, new_xc-self.x, new_yc-self.y)
        self.x = new_xc
        self.y = new_yc
        self.toile.update()


class Toile(tk.Canvas):
    def __init__(self, largeur, parent):
        tk.Canvas.__init__(self, width=largeur, height=largeur, bg="Gray80", confine=True)
        self.modele = None  #mis à jour par Root
        self.parent = parent  #fenetre principale
        self.cles_tk = []
        self.largeur = largeur

    def initialisation_graphique(self):
        """initialisation des carres initiaux
        On sauvegarde une liste des clés des objets polygones"""

        for c in self.modele.liste_carres:
            self.cles_tk.append( Carre_vue(self, c) )

    def conversion_coord_carre(self, c):
        """conversion coordonnées modèle vers tk"""
        xcentre = c.x * self.largeur
        ycentre = (1-c.y) * self.largeur
        cote = c.cote * self.largeur
        return xcentre, ycentre, cote







