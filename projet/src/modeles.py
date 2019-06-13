from random import randint
from math import sqrt, ceil
from sys import maxsize

GRIDSIZE = 30

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

    def tourne(self):
        return Vecteur(self.y, self.x)

    def __str__(self):
        return f"({self.x},{self.y})"

    def to_int(self):
        return [ int(self.x), int(self.y) ]

class Obstacle:
    def __init__(self,
                 debut=Vecteur(0, 0),
                 rayon=5):

        self.position = debut
        self.rayon = rayon

    def setPosition(self, vecteur):
        self.position = vecteur

    def getPosition(self):
        return self.position

    def getPositionGrille(self):
        i = int(self.position.x/GRIDSIZE)
        j = int(self.position.y/GRIDSIZE)
        return i,j

    def distance(self, obstacle):
        dx = self.position.x -obstacle.position.x
        dy = self.position.y -obstacle.position.y
        return sqrt( dx*dx + dy*dy )
        #return (self.position  - obstacle.position).norme()-3


class Voyageur(Obstacle):
    def __init__(self,
                 debut=Vecteur(0, 0),
                 destination=Vecteur(0, 0),
                 taille_pas=10.0):

        super().__init__(debut, rayon=10)

        self.trajet = [ debut ]
        self.destination = destination
        self.next = debut
        self.taille_pas = taille_pas

    def observation(self, carte, voyageurs = None, obstacles = None, objectif = None, cout_objectif = 0):
        ## S'il n'y a pas d'objectif, aller vers la destination
        if objectif==None:
            destination = self.destination 
        else:
            destination = objectif

        ## Vecteur vers la destination choisie
        direction = (destination - self.position)

        # Ce qui reste à parcourir
        reste = direction.norme()

        # Liste des voyageurs proches
        liste = [ voyageur
                    for voyageur in voyageurs
                    if ( (voyageur!=self) 
                         and (self.distance(voyageur) < voyageur.rayon + self.rayon + self.taille_pas) ) ]

        liste_devant = [ voyageur 
                    for voyageur in liste if (voyageur.position-destination).norme()<reste ]


        liste_obstacles = [ obstacle
                    for obstacle in obstacles
                    if ( self.distance(obstacle) < obstacle.rayon + self.rayon + self.taille_pas ) ]

        liste_obstacles_devant = [ obstacle 
                    for obstacle in liste_obstacles if (obstacle.position-destination).norme()<reste]


        t_liste_devant = len(liste_devant)
        t_liste_obstacles_devant = len(liste_obstacles_devant)
        # t_liste = len(liste)

        # Prochaine position
        if t_liste_devant==0 and t_liste_obstacles_devant==0:
            ## Aucun voyageur proche devant, on fait le deplacement optimal
            if (reste>self.taille_pas):
                pas = direction.normalise() * self.taille_pas
                # pas = Vecteur( direction.x * self.taille_pas / reste, direction.y * self.taille_pas / reste)
                self.next = self.position + pas
            else:
                self.next = destination
        else:
            ## Du monde devant
            #if objectif==None:
            i,j = self.getPositionGrille()

            ## On regarde les cases autour
            valeurs = []
            for colonne in range(i-1, i+2):
                for ligne in range(j-1, j+2):
                    centre_case = Vecteur( colonne*GRIDSIZE + GRIDSIZE/2, ligne*GRIDSIZE + GRIDSIZE/2 )
                    distance_case = (self.destination - centre_case).norme()

                    ## Cout case = nb de voyageurs dans la case + poids relatif à la distance
                    cout = carte.nb_voyageurs(colonne, ligne) + distance_case/800

                    #print(cout, cout_objectif, cout<cout_objectif)
                    if cout<=cout_objectif:
                        cout = maxsize

                    valeurs.append( (colonne, ligne, cout ) )

            #print(cout_objectif, valeurs)

            ## Recherche de la case ayant le cout le plus bas
            colonne_min, ligne_min, cout_min = min(valeurs, key=lambda x: x[2])

            if cout_min<maxsize:
                objectif = Vecteur( colonne_min*GRIDSIZE + GRIDSIZE/2, ligne_min*GRIDSIZE + GRIDSIZE/2 )
                self.observation(carte, voyageurs, obstacles, objectif, cout_min)
            else:
                self.next = self.position
        #elif t_liste>=2:
        #    ## Trop de monde, on attend
        #    self.next = self.position
        #else:
        #    ## On essaye d'eviter
        #    direction = (self.position - liste[0].position) #.tourne()
        #    pas = direction.normalise() * self.taille_pas
        #    self.next = self.position+pas

    def deplacement(self):
        self.position = self.next
        self.trajet.append(self.position)

    def arrive(self):
        return self.position == self.destination

    def getTrajet(self):
        return self.trajet

    def __str__(self):
        return f"{self.position} => {self.destination}"

class Carte:
    def __init__(self, tx=400, ty=400, nb=100):
        """Création d'une carte réctangulaire de taille tx * ty, avec nb voyageurs"""
        self.voyageurs = []
        self.voyageurs_arrives = []
        self.obstacles = []
        self.nb = nb
        self.w = tx
        self.h = ty

        #fenetre(tx+100, ty+100, "Flux")
        self.obstacles.append( Obstacle( Vecteur(tx/2, ty/2), 30) )
        self.obstacles.append( Obstacle( Vecteur(tx/6, ty/6), 30) )
        self.obstacles.append( Obstacle( Vecteur(5*tx/6, ty/6), 30) )
        self.obstacles.append( Obstacle( Vecteur(tx/6, 5*ty/6), 30) )
        self.obstacles.append( Obstacle( Vecteur(5*tx/6, 5*ty/6), 30) )

        for i in range(self.nb):

            dice = randint(0, 3)
            if dice == 0:
                dest = Vecteur(0, 0)
            elif dice == 1:
                dest = Vecteur(tx-1, 0)
            elif dice == 2:
                dest = Vecteur(tx-1, ty-1)
            else:
                dest = Vecteur(0, ty-1)

            pos = Vecteur(randint(0, tx-1), randint(0, ty-1))

            ## On crée un voyageur au hasard
            voyageur = Voyageur(pos, dest)

            ## On vérifie qu'il n'est pas trop proche de ceux déjà créés
            compteur = 1
            while compteur!=0:
                compteur = 0
                for j in range(i):
                    if voyageur.distance(self.voyageurs[j]) < 2*voyageur.rayon :
                        compteur = 1
                        voyageur.setPosition( Vecteur(randint(0, tx-1), randint(0, ty-1)) )
                        break

                for obstacle in self.obstacles:
                    if voyageur.distance( obstacle ) < voyageur.rayon + obstacle.rayon :
                        compteur = 1
                        voyageur.setPosition( Vecteur(randint(0, tx-1), randint(0, ty-1)) )
                        break

            self.voyageurs.append(voyageur)
        
        self.compter_voyageurs()

    def taille(self):
        """Renvoie la taille de la carte"""
        return self.w, self.h

    def liste_voyageurs(self):
        """Renvoie les deux listes des voyageurs"""
        return self.voyageurs, self.voyageurs_arrives

    def liste_obstacles(self):
        """Renvoie les deux listes des voyageurs"""
        return self.obstacles

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

if __name__ == '__main__':
    c = Carte(120,90,nb=5)
    c.print()
    # c.draw()

    #attendre_clic()

    for i in range(5000):
        c.step()
        if len(c.voyageurs)==0:
            break
        #attendre(50)