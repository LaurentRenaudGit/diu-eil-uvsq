from random import randint
from math import sqrt
from pyg import * # pylint: disable=import-error

DIST_SECURITE = 10

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

class Voyageur:
    def __init__(self,
                 debut=Vecteur(0, 0),
                 destination=Vecteur(0, 0),
                 dist_vision=10,
                 taille_pas=10.0):

        self.position = debut
        self.destination = destination
        self.next = debut
        self.dist_vision = dist_vision
        self.taille_pas = taille_pas

    def setPosition(self, vecteur):
        self.position = vecteur

    def distance(self, voyageur):
        return (self.position  - voyageur.position).norme()

    def observation(self, carte, voyageurs = None, obstacles = None):
        # On va essayer d'aller au plus court
        direction = (self.destination - self.position)

        # Ce qui reste à parcourir
        reste = direction.norme()

        # Liste des voyageurs proches
        liste = [ voyageur
                    for voyageur in voyageurs
                    if (not voyageur.arrive() and voyageur!=self and self.distance(voyageur) < DIST_SECURITE+self.taille_pas
                        and (voyageur.position-self.destination).norme()<reste) ]
        t_liste = len(liste)

        # Prochaine position
        if t_liste==0:
            ## Aucun voyageur proche, on fait le deplacement optimal
            if (reste>self.taille_pas):
                pas = direction.normalise() * self.taille_pas
                self.next = self.position + pas
            else:
                self.next = self.destination
        elif t_liste>=2:
            ## Trop de monde, on attend
            self.next = self.position
        else:
            ## On essaye d'eviter
            direction = (self.position - liste[0].position) #.tourne()
            pas = direction.normalise() * self.taille_pas
            self.next = self.position+pas

    def deplacement(self):
        self.position = self.next

    def draw(self):
        if not self.arrive():
            P = POINT(self.position.x+50, self.position.y+50)
            cercle_plein(P, DIST_SECURITE/2, rouge)

    def arrive(self):
        return self.position == self.destination

    def __str__(self):
        return f"{self.position} => {self.destination}"

class Obstacles:
    pass

class Carte:
    def __init__(self, tx=400, ty=400, nb=100):
        """Création d'une carte réctangulaire de taille tx * ty, avec nb voyageurs"""
        self.voyageurs = []
        self.nb = nb
        self.w = tx
        self.h = tx

        fenetre(tx+100, ty+100, "Flux")
        affiche_auto_off()

        for i in range(self.nb):

            dice = randint(0, 4)
            if dice == 0:
                dest = Vecteur(0, 0)
            elif dice == 1:
                dest = Vecteur(tx, 0)
            elif dice == 2:
                dest = Vecteur(tx, ty)
            else:
                dest = Vecteur(0, ty)

            pos = Vecteur(randint(0, tx), randint(0, ty))

            ## On crée un voyageur au hasard
            voyageur = Voyageur(pos, dest)

            ## On vérifie qu'il n'est pas trop proche de ceux déjà créés
            compteur = 1
            while compteur!=0:
                compteur = 0
                for j in range(i):
                    if (voyageur.distance(self.voyageurs[j]) ) < DIST_SECURITE :
                        compteur = 1
                        voyageur.setPosition( Vecteur(randint(0, tx), randint(0, ty)) )
                        break

            self.voyageurs.append(voyageur)

    def draw(self):
        """Dessin de la carte et des voyageurs"""
        A = POINT(50, 50)
        B = POINT(50+self.w, 50+self.h)

        remplir_ecran(noir)
        rectangle_plein(A, B, blanc)

        for i in range(self.nb):
            self.voyageurs[i].draw()

        affiche_tout()

    def step(self):
        for i in range(self.nb):
            if not self.voyageurs[i].arrive():
                self.voyageurs[i].observation(self, self.voyageurs)
                self.voyageurs[i].deplacement()
        self.draw()

    def print(self):
        """Affichage des voyageurs dans la console"""
        for i in range(self.nb):
            print("Voyageur", i, self.voyageurs[i])

if __name__ == '__main__':
    c = Carte(nb=100)
    c.print()
    c.draw()

    attendre_clic()

    for i in range(5000):
        c.step()
        attendre(50)
