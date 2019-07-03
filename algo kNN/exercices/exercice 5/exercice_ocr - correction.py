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
        d = d + abs( A[i] - B[i] )

    # On renvoie la distance calculée
    return d

def valeur( voisins ):
    """Cette fonction recoit un tableau de valeurs
    Elle doit renvoyer la valeur majoritaire."""
    
    ## On crée un tableau pour chacun des chiffres
    ## de 0 à 9 pour compter combien de fois chacun un vu
    ## Il est initialisé à 0
    compte = [0 for c in range(10) ]

    ## Le nombre de voisins
    k = len(voisins)

    ## On va noter la valeur majoritaire
    ## et le nombre de fois où on l'a vue
    majoritaire = -1
    nb = 0

    ## Pour chaque voisin
    for v in voisins:
        ## On note qu'on a vu la valeur "v"
        compte[v] += 1

        ## Si c'est majoritaire, on le note
        if compte[v] > nb:
            nb = compte[v]
            majoritaire = v
    
    ## On a fini notre decompte   
    print("Compte rendu de la recherche\n" + "-"*20)
    
    ## On passe en revue les différents chiffres
    for v in range(10):
        ## Si "v" a été vu, on affiche le pourcentage
        if compte[v] != 0:
            print(f"{ v } ({(compte[v]/k*100):.2f}%)")
    print("-"*20 + "\n")

    ## On renvoie la valeur majoritaire
    return majoritaire

## On lance l'interface en lui passant en paramètres
#      - la fonction distance ci-dessus (pour l'algo de recherche des k-voisins)
#      - la fonction valeur ci-dessus (pour déterminer la valeur choisie par kNN)
#      - la valeur de k à utiliser
application = Interface(distance, valeur, k=7)
application.run()