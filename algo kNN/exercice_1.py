from math import sqrt
import random
import matplotlib.pyplot as plt

objets = [
    (2,3, "red"),
    (3,4, "red"),
    (5,10, "red"),

    (5,2, "blue"),
    (8,5, "blue"),
    (10,1, "blue"),
]

def d(A, B):
    """A et B sont deux objets"""
    return sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 )

def classe_1nn( liste, objet):
    distance_min = float('inf')
    voisin = None

    for j in range( len(liste) ):
        distance = d(objet, liste[j])
        if distance<distance_min:
            distance_min = distance
            voisin = liste[j]

    return voisin[2]

x = [ o[0] for o in objets]
y = [ o[1] for o in objets]
c = [ o[2] for o in objets]

xp = []
yp = []
cp = []

for i in range(10000):
	o = ( random.uniform(0,10), random.uniform(0,10), None)
	xp.append( o[0] )
	yp.append( o[1] )
	cp.append( classe_1nn(objets, o) )

plt.scatter(x, y, s=64, c=c, marker="o")
plt.scatter(xp, yp, s=32, c=cp, marker="x", alpha=0.2)
plt.show()