import pygame

from modeles import Carte

class Vue:
    

if __name__ == '__main__':
    c = Carte(nb=100)
    c.print()
    c.draw()

    attendre_clic()

    for i in range(5000):
        c.step()
        attendre(50)