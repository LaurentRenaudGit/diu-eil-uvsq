import sys, pygame, random
pygame.init()

size = width, height = 1200, 800
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

class Ball:
    def __init__(self,xLoc,yLoc,diametre,xVel,yVel,couleur1,couleur2,couleur3):
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.diametre = diametre
        self.xVel = xVel
        self.yVel = yVel
        self.couleur1 = couleur1
        self.couleur2 = couleur2
        self.couleur3 = couleur3
    
    def display(self):
        fill(self.couleur1,self.couleur2,self.couleur3)
        ellipse(self.xLoc,self.yLoc,self.diametre,self.diametre)
    
    def move(self):
        self.xLoc = self.xLoc + self.xVel
        self.yLoc = self.yLoc + self.yVel
    
    def bounce(self):
        if ((self.xLoc > (width - self.diametre/2)) or (self.xLoc < self.diametre/2)):
            self.xVel = - self.xVel
        if ((self.yLoc > (height - self.diametre/2)) or (self.yLoc < self.diametre/2)):
            self.yVel = - self.yVel

ball_liste = []                        
for i in range(1000):
    temp_xVel = int(random.randint(1,10)) + 1
    temp_yVel = int(random.randint(1,10)) + 1
    ball_liste.append(Ball(50+random.randint(1,1100),50+random.randint(1,700),random.randint(1,50),temp_xVel,temp_yVel,230+random.randint(1,20),200+random.randint(1,50),random.randint(1,50)))
        

    
#    background(0,0,0)
    
for ball in ball_liste:
    if (100000<((ball.xLoc-width/2)**2+(ball.yLoc-height/2)**2)<120000):
        if (ball.xVel > 1):
            ball.xVel = ball.xVel - 1
        elif (-1<=ball.xVel<=1):
            ball.xVel = 0
        elif (ball.xVel < -1):
            ball.xVel = ball.xVel + 1
        if (ball.yVel > 1):
            ball.yVel = int(ball.yVel) - 1 
        elif (-1<=ball.yVel<=1):
            ball.yVel = 0
        elif (ball.yVel < -1):
            ball.yVel = ball.yVel + 1            
    ball.bounce()
    ball.move()
    ball.display()

        
        
