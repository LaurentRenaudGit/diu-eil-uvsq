# Exercices sur l'algorithme k-NN

## Exercice 1

On considère des points représentés par un cercle ou une croix, représentés sur la figure ci-dessous.

Les coordonnées d'un point sont ses attributs, et sa représentation graphique ( _cercle_ ou _croix_ ) est sa classe.
Ainsi le point K a pour attributs (3;4) et pour classe _croix_.

1. En appliquant l'algorithme 1-NN, attribuer une classe parmi _cercle_ ou _croix_ aux points suivant :

A(1;8), B(5;5), C(6;3), D(6;8) et E(9;6)

2. Même chose avec l'algorithme 3-NN.

3. Même chose avec l'algorithme 5-NN.


## Exercice 2

On considère des points représentés par un cercle, un triangle ou une croix, représentés sur la figure ci-dessous.

La représentation graphique d'un point ( _cercle_, _triangle_ ou _croix_ ) est sa classe.

On souhaite placer un grand nombre de points et leur attribuer une classe en appliquant l'algorithme 1-NN.
Cet algorithme étant relativement simple, on peut prévoir la future classe d'un point en fonction de sa zone d'arrivée
sur la figure.

1. À l'aide d'un crayon de couleur bleu, déterminer approximativement puis colorier la zone correspondant à la classe _cercle_ .

2. À l'aide d'un crayon de couleur vert, déterminer approximativement puis colorier la zone correspondant à la classe _triangle_ .

3. À l'aide d'un crayon de couleur rouge, déterminer approximativement puis colorier la zone correspondant à la classe _croix_ .


## Exercice 3

On considère des points caractérisés par une abscisse, une ordonnée et une couleur (**rouge** ou **vert**).
Ainsi le point A(-3,4.7,"rouge") est a pour abscisse -3, pour ordonnée 4.7, et pour couleur le rouge.

La fonction suivante a pour but de renvoyer la couleur d'un nouveau point, sous forme d'une chaîne de
caractères, en fonction des coordonnées du point et de la couleur de son plus proche voisin.
La décision se fait selon l'algorithme 1-NN.

Recopier et compléter cette fonction sachant qu'elle attend en entrée :
+ une liste de points existants, tous définis par trois valeurs (abscisse, ordonnée, couleur) de type (float, float, string).
+ un nouveau point, aussi défini par trois valeurs (abscisse, ordonnée, *None*).


```python
def classe_1nn(liste_points,point):
    distance_min = float('inf') #valeur maximale d'un flottant
    voisin = None               #initialisation du voisin
    for j in range(...):
        d = distance(point,liste_points[j]) #fonction distance renvoyant la distance (float) entre deux points
        if d < ...:
            ...
			...
    return ...
```