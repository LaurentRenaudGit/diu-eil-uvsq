import pygame

from modeles import Carte

def dessiner_carte( carte ):
    global screen

    voyageurs, arrives = carte.liste_voyageurs()

    screen.fill( [0,0,0] )

    for v in voyageurs:
        # trajet = v.getTrajet()
        # l = len(trajet)
        # if l>1:
        #     for i in range(l-1):
        #         A = trajet[i].to_int()
        #         B = trajet[i+1].to_int()
        #         pygame.draw.line(screen, [255, 0, 0], A, B)
        position = v.getPosition().to_int()
        pygame.draw.circle(screen, v.couleur, position, v.rayon)

    for o in carte.liste_obstacles():
        position = o.getPosition().to_int()
        pygame.draw.circle(screen, [255, 255, 0], position, o.rayon)

    pygame.display.flip()

def quitter():
    pygame.quit()
    exit(0)

if __name__ == '__main__':
    c = Carte(1000, 600, nb=100)
    w,h = c.taille()

    pygame.init()
    screen = pygame.display.set_mode( [w, h])
    clock = pygame.time.Clock()

    for i in range(5000):
        c.step()
        dessiner_carte( c )
        if len(c.voyageurs)==0:
            quitter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quitter()

        clock.tick(10)