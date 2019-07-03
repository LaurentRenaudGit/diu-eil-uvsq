import time

def levenshtein(chaine1, chaine2, effacement = 1, insertion = 1, substitution = 1, permutation = 1):
    """Renvoit la distance de Levenshtein entre les deux chaines passées en paramètres"""
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

f = open("french.txt")
liste = f.read().split("\n")
f.close()

# liste=liste[:5000]

print("On a %d mots en stock" % len(liste))
print("Allant de %s à %s\n" % (liste[0], liste[-1]) )

test = "odrinateir"

r = []

start = time.time()

for m in liste:
    dist = levenshtein(m, test)
    r.append( (dist, m) )

t_liste = time.time()

r.sort(key = lambda x: x[0])

t_sort = time.time()

print("Vous avez tapé '%s'" % test)

print("    voici les 10 mots les plus proches:")
for p in r[:10]:
    print("       dist. = %d : '%s'" % p )
    
print("\n Calcul des distances : %.3fs (~%d mots/sec)\n Classement des résultats : %.3fs" % (t_liste-start, len(liste)/(t_liste-start), t_sort-t_liste) )