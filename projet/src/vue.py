import pygame

from modeles import *

class Clickable():
    """Classe abstraite d'éléments cliquables"""
    def __init__(self, screen):
        self.clicked = False
        self.screen = screen

    def isIn(self, mouseX, mouseY):
        pass

    def mousePressed(self, mouseX, mouseY):
        pass

    def mouseReleased(self, mouseX, mouseY):
        pass

    def mouseMove(self, relX, relY):
        pass

    def mouseOver(self):
        pass

    def mouseLeave(self):
        pass

    def draw(self):
        pass

class Button(Clickable):
    """Une classe pour créer des boutons d'interface"""
    def __init__(self, screen, text, x, y, action):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.text = text
        self.w = 150
        self.h = 50
        self.action = action

    def isIn(self, mouseX, mouseY):
        return (mouseX >= self.x and mouseX < self.x + self.w
                and  mouseY >= self.y and mouseY < self.y + self.h)

    def mouseReleased(self, mouseX, mouseY):
        if self.isIn(mouseX, mouseY):
            self.action()

class ObstacleController(Clickable):
    """Controleur des Obstacles/Vayageurs : chargé du dessin et de l'interaction"""
    def __init__(self, screen, obstacle):
        super().__init__(screen)
        self.obstacle = obstacle
        pos = self.obstacle.getPosition()
        self.x = pos.x
        self.y = pos.y
        self.rayon = self.obstacle.rayon
        self.r2 = self.rayon * self.rayon

    def isIn(self, mouseX, mouseY):
        dx = mouseX - self.x
        dy = mouseY - self.y
        return (dx*dx+dy*dy < self.r2)

    def mouseMove(self, relX, relY):
        self.x += relX
        self.y += relY
        self.obstacle.setPosition( Vecteur(self.x, self.y) )

    def draw(self):
        if isinstance(self.obstacle, Voyageur) and self.obstacle.arrive():
            return

        self.x, self.y = self.obstacle.getPosition().to_int()
        pygame.draw.circle(self.screen, self.obstacle.couleur, [self.x, self.y], self.rayon)
        ## Dessin de la trajectoire
        # try:
        #     trajet = self.obstacle.getTrajet()
        #     l = len(trajet)
        #     if l>1:
        #         for i in range(l-1):
        #             A = trajet[i].to_int()
        #             B = trajet[i+1].to_int()
        #             pygame.draw.line(self.screen, self.obstacle.couleur, A, B)
        # except:
        #     pass

class CarteObserver:
    def __init__(self, carte):
        self.carte = carte
        self.clicked = None
        w,h = self.carte.taille()

        self.screen = pygame.display.set_mode( [w, h])
        self.clock = pygame.time.Clock()

        self.clickables = []
        voyageurs, arrives = carte.liste_voyageurs()

        for v in voyageurs:
            v_control = ObstacleController(self.screen, v)
            self.clickables.append( v_control)

        for o in carte.liste_obstacles():
            o_control = ObstacleController(self.screen, o)
            self.clickables.append( o_control)


    def redraw(self):
        self.screen.fill( [0,0,0] )

        for clickable in self.clickables:
            clickable.draw()

        pygame.display.flip()


    def run(self):
        do_loop = True

        self.redraw()

        while do_loop:
            # Si on activé un Clickable, stopper l'avancee
            if not self.clicked:
                self.carte.step()

            self.redraw()


            # Si tout le monde est arrivé, on quitte
            if len(self.carte.voyageurs)==0:
                do_loop = False

            ## Gestion des eventements
            for event in pygame.event.get():
                ## Fermeture de la fenetre
                if event.type == pygame.QUIT:
                    do_loop = False

                ## Appui sur la touche Echap
                if event.type == pygame.KEYDOWN   and event.key == pygame.K_ESCAPE:
                    do_loop = False

                ## Clic sur un bouton de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    self.clicked = None

                    ## Recherche si on clique sur un controlleur
                    for c in self.clickables:
                        if c.isIn(mx, my):
                            ## Oui : on note le controlleur
                            self.clicked = c
                            ## et on active son evenement
                            self.clicked.mousePressed(mx, my)
                            break

                ## Deplacement de la souris
                if event.type == pygame.MOUSEMOTION and self.clicked:
                    ## on active si un controlleur est actif (drag'n drop!)
                    relx, rely = event.rel
                    self.clicked.mouseMove(relx,rely)

                ## Relachement du bouton
                if event.type == pygame.MOUSEBUTTONUP:
                    ## on active un eventuelle controlleur actif
                    if self.clicked:
                        mx, my = event.pos
                        self.clicked.mouseReleased(mx, my)
                    self.clicked = None

            self.clock.tick(10)

if __name__ == '__main__':
    pygame.init()

    c = Carte(1000, 600, nb=100)
    observer = CarteObserver(c)
    observer.run()

    pygame.quit()
    exit(0)

