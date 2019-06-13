

class Test:
    """
    une classe bidon pour montrer des trucs
    """

    def __init__(self, paramCouleur, legume):
        """methode d'initialisation"""

        self.couleur = paramCouleur
        self.legume = legume

    def afficheToi(self, derniermot):
        """affiche l'objet dans la console"""

        print("ma couleur est", self.couleur, "et mon légume est", self.legume, derniermot)


    def __str__(self):
        return "ma couleur est " + self.couleur

"""
a = Test("bleu", "radis")
print(a)
a.afficheToi("au revoir")
"""

