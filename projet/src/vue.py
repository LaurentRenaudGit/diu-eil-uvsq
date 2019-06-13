import pygame

from modeles import Carte

def dessiner_carte( carte ):
    global screen

    voyageurs, arrives = carte.liste_voyageurs()

    screen.fill( [0,0,0] )

    for v in voyageurs:
        position = v.getPosition()
        pygame.draw.circle(screen, [255, 0, 0], [int(position.x), int(position.y)], v.rayon)

    for o in carte.liste_obstacles():
        position = o.getPosition()
        pygame.draw.circle(screen, [255, 255, 0], [int(position.x), int(position.y)], o.rayon)

    pygame.display.flip()

if __name__ == '__main__':
    c = Carte(800, 600, nb=100)
    w,h = c.taille()

    pygame.init()
    screen = pygame.display.set_mode( [w, h])
    clock = pygame.time.Clock()

    for i in range(5000):
        c.step()
        dessiner_carte( c )
        if len(c.voyageurs)==0:
            pygame.quit()
        clock.tick(10)