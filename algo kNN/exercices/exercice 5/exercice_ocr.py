from interface import Interface

def distance(A, B):
    """A et B sont deux tableaux de même taille
    Chaque case correspond à la valeur d'un pixel entre 0 et 255
    
    Compléter la fonction pour qu'elle renvoie la somme des écarts entre 
    les pixels des deux tableaux
    
    Remqarque:
      Si un pixel de A contient 12 et celui de B contient 20, l'écart est 8.
      Si un pixel de A contient 12 et celui de B contient 4,  l'écart est *aussi* 8.
    """
    # La taille des deux tableaux
    nb_pixels = len(A)

    # De base, la distance est supposée nulle
    d = 0

    # On passe en revue chaque pixel
    for i in range(nb_pixels):
        # Comparer le pixel A[i] et le pixel B[i]
        ...

    # On renvoie la distance calculée
    return d

def valeur( voisins ):
    """Cette fonction recoit un tableau de valeurs
    Elle doit renvoyer la valeur majoritaire."""

    for v in voisins:
        print("Un des voisins vaut", v)

    return 0

## On lance l'interface en lui passant en paramètres
#      - la fonction distance ci-dessus (pour l'algo de recherche des k-voisins)
#      - la fonction valeur ci-dessus (pour déterminer la valeur choisie par kNN)
#      - la valeur de k à utiliser
application = Interface(distance, valeur, k=7)
application.run()