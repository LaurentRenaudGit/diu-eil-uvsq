import time

def levenshtein(chaine1, chaine2, effacement = 1, insertion = 1, substitution = 1, permutation = 1):
    """Renvoie la distance de Levenshtein entre les deux chaines passées en paramètres"""
    l1 = len(chaine1)
    l2 = len(chaine2)

    d = [ [0 for c in range( l2+1 ) ] for l in range( l1+1 ) ]
    
    for i in range( l1+1 ):
        d[i][0] = i
    
    for j in range( l2+1 ):
        d[0][j] = j
        
    for i in range(1, l1+1):
        for j in range(1, l2+1):
            if chaine1[i-1] == chaine2[j-1]:
                cout = 0
            else:
                cout = substitution
            d[i][j] = min( d[i-1][j] + effacement,      # effacement du nouveau caractère de chaine1
                           d[i][j-1] + insertion,       # insertion dans chaine2 du nouveau caractère de chaine1
                           d[i-1][j-1] + cout           # substitution
                         )
            # Permutation
            if i > 1 and j > 1 and chaine1[i-1] == chaine2[j-2] and chaine1[i-2] == chaine2[j-1]:
                d[i][j] = min( d[i][j], d[i-2][j-2] + permutation )

    return d[l1][l2]

f = open("liste_francais_propre.txt")
liste = f.read().split("\n")
f.close()

# liste=liste[:5000]

print("On a %d mots français en stock" % len(liste))
print("Allant de %s à %s\n" % (liste[0], liste[-1]) )

f = open("english.txt")
liste2 = f.read().split("\n")
f.close()

print("On a %d mots anglais en stock" % len(liste2))
print("Allant de %s à %s\n" % (liste2[0], liste2[-1]) )

mot_test = input("Quel mot voulez-vous tester ?")

k = int(input("Valeur de k de l'algorithme k-NN ?"))

r = []

start = time.time()

for m in liste:
    dist = levenshtein(m, mot_test)
    r.append( (dist, m, -1) ) # -1 pour français

for m in liste2:
    dist = levenshtein(m, mot_test)
    r.append( (dist, m, 1) ) # 1 pour anglais

t_liste = time.time()

r.sort(key = lambda x: x[0])

t_sort = time.time()

print("Vous avez tapé '%s'" % mot_test)

print("    voici les "+str(k)+" mots les plus proches:")
compteur = 0
mot_trouve = False
for p in r[:k]:
    """ si on a trouvé le mot (distance = 0)
    """
    if (p[0]==0 and p[2]==-1):
        mot_trouve = True
        langue = "français"
    elif (p[0]==0 and p[2]==1):
        mot_trouve = True
        langue = "anglais"
    else:
        """ on incrémente le compteur
            avec ou sans pondération en 1/dist
        """
        #compteur = compteur + p[2]
        compteur = compteur + p[2]/p[0]
    if p[2]==-1:
        print("          dist. "+str(p[0])+" de "+p[1]+" en français")
    else:
        print("          dist. "+str(p[0])+" de "+p[1]+" en anglais")

print(compteur)
if (mot_trouve):
    print("Le mot "+mot_test+" est "+langue+".")    
elif compteur > 0:
    print("Le mot "+mot_test+" est anglais"+".")
else:
    print("Le mot "+mot_test+" est français"+".")

    
print("\n Calcul des distances : %.3fs (~%d mots/sec)\n Classement des résultats : %.3fs" % (t_liste-start, len(liste)/(t_liste-start), t_sort-t_liste) )
