from interface import Interface

def distance(A, B):
    """A et B sont deux tableaux de même taille
    Chaque case correspond à la couleur d'un pixel 0=Blanc / 1=Noir
    
    Compléter la fonction pour qu'elle renvoie le nombre de pixels différents
    entre les deux tableaux"""
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

## On lance l'interface en lui passant les 2 fonctions précédentes
application = Interface(distance, valeur, k=9)
application.run()