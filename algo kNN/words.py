def levenshtein(chaine1, chaine2):
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
                cout = 1
            d[i][j] = min( d[i-1][j] + 1,       # effacement du nouveau caractère de chaine1
                           d[i][j-1] + 1,       # insertion dans chaine2 du nouveau caractère de chaine1
                           d[i-1][j-1] + cout   # substitution
                         )
    print(d)
    
    return	d[l1][l2]
    """d est un tableau de longueurChaine1+1 rangées et longueurChaine2+1 colonnes
      d est indexé à partir de 0, les chaînes à partir de 1
      déclarer entier d[0..longueurChaine1, 0..longueurChaine2]
	  i et j itèrent sur chaine1 et chaine2
    déclarer entier i, j, coûtSubstitution
 
   pour i de 0 à longueurChaine1
       d[i, 0] := i
   pour j de 0 à longueurChaine2
       d[0, j] := j
 
   pour i de 1 à longueurChaine1
      pour j de 1 à longueurChaine2
          si chaine1[i-1] = chaine2[j-1] alors coûtSubstitution := 0
                                     sinon coûtSubstitution := 1    
           d[i, j] := minimum(
                                d[i-1, j  ] + 1,                 // effacement du nouveau caractère de chaine1
                                d[i,   j-1] + 1,                 // insertion dans chaine2 du nouveau caractère de chaine1
                                d[i-1, j-1] + coûtSubstitution   // substitution
                             )
 
   renvoyer d[longueurChaine1, longueurChaine2]"""
   
print( levenshtein("niche", "chiens") )