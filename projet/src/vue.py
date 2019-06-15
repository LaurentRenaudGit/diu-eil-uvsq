import pygame

from modeles import *

class Clickable():
    """Classe abstraite d'éléments cliquables"""
    def __init__(self, screen):
        self.clicked = False
        self.screen = screen
        self.action = False
        self.hover = False

    def isIn(self, mouseX, mouseY):
        pass

    def mousePressed(self, mouseX, mouseY):
        pass

    def mouseReleased(self, mouseX, mouseY):
        pass

    def mouseMove(self, relX, relY):
        pass

    def mouseOver(self):
        self.hover = True

    def mouseLeave(self):
        self.hover = False

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
        self.h = 30
        self.action = action
        self.color = [100, 100, 100]

    def isIn(self, mouseX, mouseY):
        return (mouseX >= self.x and mouseX < self.x + self.w
                and  mouseY >= self.y and mouseY < self.y + self.h)

    def mouseReleased(self, mouseX, mouseY):
        if self.isIn(mouseX, mouseY):
            self.action()

    def draw(self):
        pygame.draw.rect( self.screen, self.color, [self.x, self.y, self.w, self.h] )
        font = pygame.font.SysFont('Helvetica', 20)
        text_surface = font.render(self.text, False, (255, 255, 255))
        self.screen.blit(text_surface, (self.x+5, self.y+2))

    def mouseOver(self):
        self.hover = True
        self.color = [128, 128, 128]

    def mouseLeave(self):
        self.hover = False
        self.color = [96, 96, 96]

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
        dx = mouseX - (self.x)
        dy = mouseY - (self.y)
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

PAUSE = 0
PLAY  = 1

class CarteObserver:
    def __init__(self, carte):
        self.carte = carte
        self.clicked = None
        self.w = self.h = 0
        self.mode = PAUSE

        self.w, self.h = self.carte.taille()

        ## Création d'une fenetre avec une marge + 40px pour le menu
        pygame.display.set_caption("Simulateur de foule")
        self.screen = pygame.display.set_mode( [self.w, self.h + 40])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Helvetica', 16)

        self.clickables = []
        voyageurs, arrives = carte.liste_voyageurs()

        for v in voyageurs:
            v_control = ObstacleController(self.screen, v)
            self.clickables.append( v_control)

        for o in carte.liste_obstacles():
            o_control = ObstacleController(self.screen, o)
            self.clickables.append( o_control)

        ## Menu
        self.menu = []
        ## Bouton 1 = Play / Pause
        bouton = Button(self.screen, "Lancer", 10, self.h+5, self.togglePause)
        self.menu.append(bouton)

        bouton = Button(self.screen, "Une étape", 170, self.h+5, self.advance)
        self.menu.append(bouton)

        ## Ajout du menu au elements clickables
        self.clickables += self.menu

    def togglePause(self):
        b = self.menu[0]
        if b.text == "Lancer":
            self.mode = PLAY
            b.text = "Pauser"
        else:
            self.mode = PAUSE
            b.text = "Lancer"

    def advance(self):
        b = self.menu[0]
        self.mode = PAUSE
        b.text = "Lancer"
        self.carte.step()

    def redraw(self):
        self.screen.fill( [0, 0, 0])

        ## Dessin des objets de la simulation
        for clickable in self.clickables:
            if not clickable.action:
                clickable.draw()

        ## Dessin du menu
        pygame.draw.rect( self.screen, [64, 64, 64], [0, self.h, self.w, 40] )
        for bouton in self.menu:
            bouton.draw()

        pygame.display.flip()


    def run(self):
        do_loop = True

        self.redraw()

        while do_loop:
            # Si on activé un Clickable, stopper l'avancee
            if not self.clicked and self.mode == PLAY:
                self.carte.step()

            # Rafraichissement de l'ecran
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
                if event.type == pygame.MOUSEMOTION:
                    if self.clicked: ## on active si un controlleur est actif (drag'n drop!)
                        relx, rely = event.rel
                        self.clicked.mouseMove(relx,rely)

                    ## Evenement "mouseover"
                    mx, my = event.pos
                    for c in self.clickables:
                        if c.isIn(mx, my):
                            c.mouseOver()
                        elif c.hover:
                            c.mouseLeave()

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
    pygame.font.init()

    c = Carte(1000, 600, nb=100)
    observer = CarteObserver(c)
    observer.run()

    pygame.quit()
    exit(0)

