import pygame
import threading

_ZF = 12    ## Facteur de zoom de la zone de dessin
_W  = 64    ## Taille de la zone de dessins en pixels
            ##    on va en extraire un dessin de 16x16 pixels après mise à l'échelle
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRIS  = (200,200,200)

class Chiffre():
    def __init__(self):
        self.pixels = [ ]
        self.valeur = -1
    
    def draw(self, screen, dx, dy):
        for x in range(16):
            for y in range(16):
                if self.pixels[x+16*y]==0:
                    color = WHITE
                else:
                    color = BLACK
                
                pygame.draw.rect( screen, color, (x*2 + dx, y*2 + dy, 2, 2) )
        
            
class Drawing():
    def __init__(self):
        self.pixels = [ [0 for i in range(_W) ]  for i in range(_W) ]
        self.color = None
        
    def draw(self, screen):
        for x in range(_W):
            for y in range(_W):
                if self.pixels[x][y]==0:
                    color = WHITE
                else:
                    color = BLACK
                
                ## Version zoomee
                pygame.draw.rect( screen, color, (x*_ZF, y*_ZF, _ZF, _ZF) )
                
                ## Version normale
                pygame.draw.rect( screen, color, (_W*_ZF+ 5 + x, y, 1, 1) )
                
    def pen_up(self):
        self.ox = None
        self.color = None
        
    def paint(self,x,y):
        ## 5x5
        for dx in range(-2,3):
            for dy in range(-2,3):
                if x+dx>=0 and x+dx<_W and y+dy>=0 and y+dy<_W and abs(dx)+abs(dy)!=4:
                    self.pixels[x+dx][y+dy] = self.color
        ## 3x3
        #for dx in range(-1,2):
        #    for dy in range(-1,2):
        #        if x+dx>=0 and x+dx<_W and y+dy>=0 and y+dy<_W:
        #            self.pixels[x+dx][y+dy] = self.color
                
    def move(self, mx, my):
        mx = mx // _ZF
        my = my // _ZF
        
        ## On évite de dessiner en dehors
        if self.color == None or mx<0 or my<0 or mx>=_W or my>=_W:
            self.ox = None
            return

        if self.ox != None and (self.ox!=mx or self.oy!=my):
            dx = mx-self.ox
            dy = my-self.oy
            if abs(dx) > abs(dy):
                x = self.ox
                while x != mx:
                    y = int( self.oy + (x-self.ox)*(dy)/dx  )
                    self.paint(x,y)
                    x += (1 if dx>0 else -1)
            else:
                y = self.oy
                while y != my:
                    x = int( self.ox + (y-self.oy)*(dx)/dy  )
                    self.paint(x,y)
                    y += (1 if dy>0 else -1)
                    
        self.paint(mx,my)
        
        self.ox = mx
        self.oy = my
                
    def click(self, mx, my):
        mx = mx // _ZF
        my = my // _ZF
        
        ## On évite de dessiner en dehors
        if mx<0 or my<0 or mx>=_W or my>=_W:
            return
        
        self.color = 1-self.pixels[mx][my]
        self.ox = mx
        self.oy = my
        self.paint(mx,my)

    def clip(self):
        """Cette fonction transforme la zone de dessin non vierge en image 16x16
        sous forme de tableau exploitable par la classe Chiffre"""
        data   = []
        
        # Recherche du pixel le plus à gauche
        mx = -1
        done = False
        while not done:
            mx += 1
            if mx==_W:
                return [ 0 for i in range(256) ]
            for y in range(_W):
                if self.pixels[mx][y] != 0:
                    done = True
                    break
        
        # Recherche du pixel le plus à droite
        Mx = _W
        done = False
        while not done:
            Mx -= 1
            for y in range(_W):
                if self.pixels[Mx][y] != 0:
                    done = True
                    break
    
        # Recherche du pixel le plus haut
        my = -1
        done = False
        while not done:
            my += 1
            for x in range(_W):
                if self.pixels[x][my] != 0:
                    done = True
                    break
        
        # Recherche du pixel le plus bas
        My = _W
        done = False
        while not done:
            My -= 1
            for x in range(_W):
                if self.pixels[x][My] != 0:
                    done = True
                    break
      
        # Calcul de la taille de la zone à transformer en 16x16      
        cropSize = max(Mx-mx, My-my)
        mx = (mx+Mx-cropSize)//2
        my = (my+My-cropSize)//2
    
        ns = 16
        cropSize += 1
        
        # Changement d'échelle
        for y in range(ns):
            oy = my + y*cropSize//ns
            for x in range(ns):
                ox = mx + x*cropSize//ns
                
                if (ox<0 or ox >= _W or oy<0 or oy >= _W):
                    data.append(0)
                else:
                    v = self.pixels[ox][oy]
                    if (v==0):
                        data.append(0)
                    else:
                        data.append(1)
    
        return data
        
class VoisinThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.stop_event = threading.Event()
        
    def run(self):
        """Cette fonction calcule dans un thread les k voisins les plus proches de 'test' dans la 'base'.
        test est un tableau de pixels représentant un chiffre
        base est un tableau dont les éléments sont des objets de classe Chiffre"""
        
        d = self.parent.f_distance
        bdd = self.parent.bdd
        test = self.parent.test
        k = self.parent.k
    
        ## Recherche de la distance minimale : on initialise avec les k-premières valeurs
        ##   du tableau base
        temp = [ (bdd[i], d( test.pixels, bdd[i].pixels) ) for i in range(k) ]
        temp.sort( key = lambda x: x[1] )
        ## La dernière case est la pire (distance la plus grande pour le moment)
        worst_d = temp[k-1][1]
        
        ## Dessin des voisins en cours
        for i in range(k):
            temp[i][0].draw(self.parent.screen, _ZF*_W + (_W+5-32)//2, 2 *_W + 36*i )
        
        i = k+1
    
        # On passe en revue les valeurs suivantes
        while i<len(bdd) and not self.stop_event.isSet():
            dist = d(test.pixels, bdd[i].pixels)
            
            ## On est tombé sur un élément plus proche ?
            if dist<worst_d:
                temp[k-1] = (bdd[i], dist)

                ## On retrie...
                temp.sort( key = lambda x: x[1] )
                worst_d = temp[k-1][1]

                ## On redessine
                for j in range(k):
                    temp[j][0].draw(self.parent.screen, _ZF*_W + (_W+5-32)//2, 2 *_W + 36*j )
            
            i += 1                

        if not self.stop_event.isSet():
            resultat = [ t[0] for t in temp ]
            self.parent.found( resultat )
        
    def stop(self):
        self.stop_event.set()

  
class Interface():
    def __init__(self, f_distance, f_valeur, k=1, N=10000):
        assert k<=15, "k doit valoir au maximum 15"
        assert N<=10000, "Il n'y a que 10000 valeurs connues, N ne peut pas être supérieur"
    
        self.f_distance = f_distance
        self.f_valeur = f_valeur
        self.k = k
        self.bdd = []
        self.thread = None
        
        ## Lecture des chiffres du fichier
        print("Lecture de la base de donnée de valeurs connues...")
        
        im_file = open("images.raw", "rb")
        vl_file = open("valeurs.raw", "rb")
        vl_file.seek(8)
        
        for i in range(N):
            c = Chiffre()
        
            # Chaque chiffre est codé sur 32 octets
            for y in range(32):
                # Lecture d'un octet
                v = ord( im_file.read(1) )
                
                # Lecture des 8 bits pour former les pixels
                for i in range(8):
                    b = ( v >> (7-i) ) & 1
                    c.pixels.append(b)

            c.valeur = ord( vl_file.read(1) )
            
            self.bdd.append(c)
        
        im_file.close()
        vl_file.close()
        
        print(f"Lecture finie, {N} valeurs en mémoire")
        
    def found(self, data):
        v = self.f_valeur( [ d.valeur for d in data ] )
        font = pygame.font.SysFont('Helvetica', _W*2//3)
        pygame.draw.rect(self.screen, GRIS, ( _ZF*_W + 2, _W+2, _W, _W*2//3) )
        text = font.render( "=" + str(v) + "?", False, (255, 0, 0) )
        self.screen.blit(text, ( _ZF*_W +2, _W+2) )

    def check_events(self):
        for event in pygame.event.get():
            ## Fermeture de la fenetre
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN  and event.key == pygame.K_ESCAPE):
                self.do_loop = False

            ## Clic sur un bouton de la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                self.drawing.click(mx,my)
                
                ## Si on a dessiné qq chose, lancer une recherche de voisin
                if self.drawing.color != None:
                    if self.thread:
                        self.thread.stop()
                    self.thread = VoisinThread( self )
                    self.thread.start()

            ## Deplacement de la souris
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                self.drawing.move(mx, my)
                
                ## Si on a dessiné qq chose, lancer une recherche de voisin
                if self.drawing.color != None:
                    if self.thread:
                        self.thread.stop()
                    self.thread = VoisinThread( self )
                    self.thread.start()
        
            ## Relachement de la souris
            if event.type == pygame.MOUSEBUTTONUP:
                self.drawing.pen_up()
                        
    def run(self):
        ## Initialisation de la fenetre de dessin
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode( (_ZF*_W + 5 + _W , _ZF*_W) )
        self.screen.fill( GRIS )
        self.drawing = Drawing()
        
        self.do_loop = True
        self.color = None
        
        self.test = Chiffre()

        while self.do_loop:
            ## Check
            self.test.pixels = self.drawing.clip()
        
            ## Dessin
            self.drawing.draw(self.screen)
            pygame.display.flip()
    
            ## Events
            self.check_events()
            
            ## Doit on chercher les voisins ?
            #if self.drawing.color:
            #    print("Yes")

            self.clock.tick(20)
            
        ## On tue le thread éventuel
        if self.thread:
            self.thread.stop()
