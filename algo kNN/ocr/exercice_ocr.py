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
    d = 0
    for i in range( len(A) ):
        d += abs( A[i] - B[i] )
    
    return d

def valeur( voisins ):
    """Cette fonction recoit un tableau de valeurs
    Elle doit renvoyer la valeur majoritaire."""
    
    compte = [ [c,0] for c in range(10) ]
    total = 0

    for v in voisins:
        compte[v][1] += 1
        total += 1
    
    compte.sort( key = lambda x: -x[1] )
    
    print("Compte rendu de la recherche\n" + "-"*20)
    
    for c in compte:
        chiffre, effectif = c
        if effectif != 0:
            print(f"{ chiffre } ({(effectif/total*100):.2f}%)")
    
    print("-"*20 + "\n")
    
    return compte[0][0]

## On lance l'interface en lui passant en paramètres
#      - le fichier contenant des images de chiffres connus
#      - la fonction distance ci-dessus (pour l'algo de recherche des k-voisins)
#      - la fonction valeur ci-dessus (pour déterminer la valeur choisie par kNN)
#      - la valeur de k à utiliser
application = Interface("images-cropped_16px_2bpp.raw", distance, valeur, k=7)
application.run()