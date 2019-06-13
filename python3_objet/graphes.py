

class Sommet:
    """stocke un sommet du graphe"""

    def __init__(self, nom = None):
        self.nom = nom


class Arc:
    """represente un arc du graphe"""

    def __init__(self, pdebut, pfin):
        """pdebut et pdfin sont des objets Sommet"""
        #assert isinstance(pdebut, Sommet)
        self.extremites = [pdebut, pfin]

    def __str__(self):
        return "arc de début " + str(self.extremites[0].nom) + " et de fin " + str(self.extremites[1].nom)

    def getDebut(self):
        return self.extremites[0]

    def setFin(self, nouvelle_fin):
        self.extremites[1] = nouvelle_fin


class Graphe:
    """stocke un graphe oriente"""

    def __init__(self, nom = None):
        self.nom = nom
        self.sommets = []   #liste de Sommets
        self.arcs = []    #liste d'Arcs

    def ajouter_sommet(self, nom_du_sommet):
        """crée et ajoute un sommet au graphe"""

        s = Sommet(nom_du_sommet)
        self.sommets.append(s)

    def ajouter_arc(self, debut, fin):
        self.arcs.append( Arc(debut, fin) )

    def degre_sortant(self, sommet):
        compteur = 0
        for arc in self.arcs:
            if arc.getDebut() == sommet:
                compteur += 1
        return compteur

        return len([ arc for arc in self.arcs if arc.getDebut() == sommet ])




g = Graphe()
g.ajouter_sommet("titi")
s1 = Sommet("hop")
s2 = Sommet("hip")
g.ajouter_arc(s1, s2)
print(g.sommets)




