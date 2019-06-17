from random import randint
from math import sqrt, ceil
from sys import maxsize

GRIDSIZE = 30
BLUE = (0,0,255)
RED = (255,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

class Vecteur:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vecteur(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vecteur(self.x - other.x, self.y - other.y)

    def __mul__(self, k):
        return Vecteur(k*self.x, k*self.y)

    def __div__(self, k):
        return Vecteur(self.x/k, self.y/k)

    def norme(self):
        return sqrt(self.x**2 + self.y**2)

    def normalise(self):
        n = self.norme()
        return Vecteur(self.x/n, self.y/n)

    def __str__(self):
        return f"({self.x},{self.y})"

    def to_int(self):
        return [ int(self.x), int(self.y) ]

class Obstacle:
    def __init__(self,
                 debut=Vecteur(0, 0),
                 rayon=5,
                 couleur=YELLOW,
                 sortie = False):

        self.position = debut
        self.rayon = rayon
        self.couleur = couleur
        self.sortie = sortie

    # Methode publique
    def setPosition(self, vecteur):
        self.position = vecteur

    # Methode publique
    ## Fix : renvoyer une copie pour protéger la position ?
    def getPosition(self):
        return self.position

    def getPositionGrille(self):
        i = int(self.position.x/GRIDSIZE)
        j = int(self.position.y/GRIDSIZE)
        return i,j

    def distance(self, obstacle):
        return (self.position  - obstacle.position).norme()

class Voyageur(Obstacle):
    def __init__(self,
                 debut,
                 destination,
                 taille_pas=10.0,
                 couleur=BLUE):

        super().__init__(debut, rayon=10, couleur=couleur)

        self.trajet = [ debut ]
        self.destination = destination
        self.next = debut
        self.taille_pas = taille_pas
        self.arrivee_atteinte = False

    def observation(self, carte, voyageurs = None, obstacles = None, objectif = None, cout_objectif = 0):
        ## S'il n'y a pas d'objectif, aller vers la destination
        if objectif==None:
            destination = self.destination.position
        else:
            destination = objectif

        ## Vecteur vers la destination choisie
        direction = (destination - self.position)

        # Ce qui reste à parcourir
        reste = direction.norme()

        # debug
        if (reste>self.taille_pas):
            pas = direction.normalise() * self.taille_pas
            # pas = Vecteur( direction.x * self.taille_pas / reste, direction.y * self.taille_pas / reste)
            cible = self.position + pas
        else:
            cible = destination
        
        # Nombre des voyageurs trop proches
        nb_voyageurs_proches = len( [ voyageur 
                for voyageur in voyageurs
                if ( voyageur!=self
                     and self.distance(voyageur) < voyageur.rayon + self.rayon + self.taille_pas 
                     and (cible - voyageur.position).norme() < self.rayon + voyageur.rayon) ] )

        # Nombre des obstacles trop proches
        nb_obstacles_proches = len( [ obstacle
                for obstacle in obstacles
                if ( self.distance(obstacle) < obstacle.rayon + self.rayon + self.taille_pas
                      and (cible - obstacle.position).norme() < self.rayon + obstacle.rayon) ] )

        if nb_voyageurs_proches==0 and nb_obstacles_proches==0:
            ## Aucune obstruction, on fait le deplacement optimal
            self.next = cible
        else:
            ## Du monde devant
            i,j = self.getPositionGrille()

            ## On regarde les cases autour
            valeurs = []
            for colonne in range(i-1, i+2):
                for ligne in range(j-1, j+2):
                    ## On saute la case où on est déja
                    if (i==colonne and j==ligne):
                        continue
                    centre_case = Vecteur( colonne*GRIDSIZE + GRIDSIZE/2, ligne*GRIDSIZE + GRIDSIZE/2 )
                    distance_case = (self.destination.position - centre_case).norme()

                    ## Cout case = nb de voyageurs dans la case + poids relatif à la distance
                    cout = carte.nb_voyageurs(colonne, ligne) + distance_case/800

                    ## Si ce n'est pas la première tentative, on élimine celles déjà testées
                    if cout<=cout_objectif:
                        cout = maxsize

                    valeurs.append( (colonne, ligne, cout ) )

            ## Recherche de la case ayant le cout le plus bas
            colonne_min, ligne_min, cout_min = min(valeurs, key=lambda x: x[2])

            if cout_min<maxsize:
                objectif = Vecteur( colonne_min*GRIDSIZE + GRIDSIZE/2, ligne_min*GRIDSIZE + GRIDSIZE/2 )
                self.observation(carte, voyageurs, obstacles, objectif, cout_min)
            else:
                self.next = self.position

    def deplacement(self):
        self.position = self.next
        self.trajet.append(self.position)
        if self.position == self.destination.position:
            self.arrivee_atteinte = True

    ## Methode publique
    def arrive(self):
        return self.arrivee_atteinte

    ## Methode publique
    def getTrajet(self):
        return self.trajet

    def __str__(self):
        return f"{self.position} => {self.destination.position}"

class Carte:
    def __init__(self, tx=400, ty=400):
        """Création d'une carte rectangulaire de taille tx * ty, avec nb voyageurs"""
        self.voyageurs = []
        self.voyageurs_arrives = []
        self.obstacles = []
        self.arrivees = []
        self.nb = 0
        self.w = tx
        self.h = ty


    def reset(self):
        self.voyageurs = []
        self.voyageurs_arrives = []
        self.obstacles = []
        self.arrivees = []
        self.nb = 0

    def ajouter_arrivee(self, x, y, couleur):
        arrivee = Obstacle( Vecteur(x, y), 10, couleur = couleur, sortie=True)
        self.arrivees.append( arrivee )

        return arrivee

    def ajouter_obstacle(self, x, y):
        obstacle = Obstacle( Vecteur(x, y), 30)
        self.obstacles.append( obstacle )

        return obstacle

    def ajouter_voyageur(self, x, y, arrivee, check_obstacles = False):
        voyageur = Voyageur( Vecteur(x,y), arrivee, couleur=arrivee.couleur)

        ## On vérifie si c'est ok comme position de voyageur...
        if check_obstacles:
            for v in self.voyageurs:
                if voyageur.distance( v ) < 2*voyageur.rayon:
                    return None
            for o in self.obstacles:
                if voyageur.distance( o ) < voyageur.rayon + o.rayon:
                    return None

        voyageur = Voyageur( Vecteur(x,y), arrivee, couleur=arrivee.couleur)
        self.voyageurs.append( voyageur )

        return voyageur

    def taille(self):
        """Renvoie la taille de la carte"""
        return self.w, self.h

    def liste_voyageurs(self):
        """Renvoie les deux listes des voyageurs"""
        return self.voyageurs, self.voyageurs_arrives

    def liste_obstacles(self):
        """Renvoie la liste des obstacles"""
        return self.obstacles

    def liste_arrivees(self):
        """Renvoie la liste des arrivees"""
        return self.arrivees

    def step(self):
        for v in self.voyageurs:
            v.observation(self, self.voyageurs, self.obstacles)
            v.deplacement()
        
        ## Enlever les voyageurs arrivés à destination
        for v in self.voyageurs:
            if v.arrive():
                self.voyageurs.remove(v)
                self.voyageurs_arrives.append(v)

        self.compter_voyageurs()

    def compter_voyageurs(self):
        nb_colonnes = ceil(self.w / GRIDSIZE)
        nb_lignes = ceil(self.h / GRIDSIZE)
        #print(nb_colonnes, nb_lignes)
        self.grille_nb_voyageurs = [ [ 0 ]*nb_lignes for i in range(nb_colonnes) ]

        for v in self.voyageurs:
            i,j = v.getPositionGrille()
            self.grille_nb_voyageurs[i][j] += 1

        #print(self.grille_nb_voyageurs)

    def print(self):
        """Affichage des voyageurs dans la console"""
        for i in range(self.nb):
            print("Voyageur", i, self.voyageurs[i])

    def nb_voyageurs(self, i, j):
        """Renvoie le nombre de voyageurs dans la case (i,j) de la carte.
        Une case représéente un carré de 3x3 mètres = 30x30 px"""
        nb_colonnes = ceil(self.w / GRIDSIZE)
        nb_lignes = ceil(self.h / GRIDSIZE)

        ## Si (i,j) est en dehors de la grille, on renvoie maxsize
        if i<0 or i>=nb_colonnes or j<0 or j>=nb_lignes:
            return maxsize

        return self.grille_nb_voyageurs[i][j]