import pygame as pg
from pygame.locals import (K_LEFT, K_RIGHT) # Importerer knapper, å bruke 
import time
# Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
VINDU_BREDDE = 600
VINDU_HOYDE  = 700
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])

# Angir hvilken skrifttype og tekststørrelse vi vil bruke på tekst
font = pg.font.SysFont("Arial", 24)
score = 0

# Klasse for ballen 
class Ball:
  """Klasse for å representere en ball"""
  def __init__(self, x, y, farty, fartx, radius, vindusobjekt):
    """Konstruktør"""
    self.x = x
    self.y = y
    self.farty = farty
    self.fartx = fartx
    self.radius = radius
    self.vindusobjekt = vindusobjekt
  def tegn(self):
    """Metode for å tegne ballen"""
    pg.draw.circle(self.vindusobjekt, (255, 69, 0), (self.x, self.y), self.radius) 

  def flytt(self):
    """Metode for å flytte ballen"""
    # Sjekker om ballen er utenfor høyre/venstre kant
    if ((self.x - self.radius) <= 0) or ((self.x + self.radius) >= self.vindusobjekt.get_width()):
      self.fartx = -self.fartx
    elif ((self.y - self.radius) <= 0) or ((self.y + self.radius) >= self.vindusobjekt.get_height()):
        self.farty = -self.farty

    # Flytter ballen
    self.y += self.farty
    self.x += self.fartx


# Paddle klasse
class Paddle:
    """Paddle for multipong"""
    def __init__(self, x1, y1, x2, y2, fart, størrelse, farge, vindusobjekt):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.fart = fart
        self.størrelse = størrelse
        self.farge = farge
        self.vindusobjekt = vindusobjekt
    
    def tegn(self):
        pg.draw.line(self.vindusobjekt, self.farge, (self.x1, self.y1), (self.x2, self.y2), self.størrelse)

    # Kollisjon av paddene venstre og høyre av skjermen
    def kollisjon(self):
        if (self.x1 <= 0):
            self.x2 = 101
            self.x1 = 1
        elif (self.x2 >= self.vindusobjekt.get_width()):
            self.x2 = self.vindusobjekt.get_width() -1
            self.x1 = self.vindusobjekt.get_width() - 101

    # Funksjon som flytter padden venstre og høyre
    def flytt(self, taster):
        if (self.x1 <= 0 or self.x2 >= self.vindusobjekt.get_width()):
            self.fart = 0

        if taster[K_LEFT]:
            self.x1 -= self.fart
            self.x2 -= self.fart
        if taster[K_RIGHT]:
            self.x1 += self.fart
            self.x2 += self.fart



# Lager et Ball-objekt
ball = Ball(250, 250, 0.3, 0.3, 15, vindu)
ball2 = Ball(100,100,0.3,0.3,15,vindu)
paddle = Paddle(200, 660, 300, 660, 0.5 , 15, (0, 255, 0), vindu)

# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:

    def restart():
        ball.x, ball.y = 250, 250 
        ball.fartx, ball.farty = 0.3, 0.3
        global score
        score = 0
            
    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                fortsett = False
            if event.key == pg.K_r:
                restart()

    # Farger bakgrunnen lyseblå
    vindu.fill((135, 206, 235))

    #Taster
    taster = pg.key.get_pressed()
    # Tegner og flytter ballen
    ball.tegn()
    ball.flytt()

    # ball2.tegn()
    # ball2.flytt()
    # Tegner og flytter paddelen
    paddle.tegn()
    paddle.flytt(taster)
    paddle.kollisjon()

    # Ball kollisjon med paddle

    if((ball.y + ball.radius) >= 660 and (ball.y + ball.radius) <= 670 and (ball.x + ball.radius) >= paddle.x1 and (ball.x + ball.radius) <= paddle.x2):
        score = score + 1
        ball.farty = -ball.farty
        ball.fartx = +ball.fartx
    
    # Hvis ballen treffer bunnen, så får man muligheten til å restarte spillet eller avslutte det. Stopper også ballen fra og bevege seg
    if ((ball.y + ball.radius) >= 700):
        ball.fartx = 0
        ball.farty = 0
        bilde = font.render("Trykk (R) for å starte på nytt ", True, (250, 250, 250))
        bilde2 = font.render("Trykk (ESC) for å avslutte spill", True, (250, 250, 250))
        bilde3 = font.render("Du tapte", True, (250, 250, 250))
        vindu.blit(bilde3, ((VINDU_BREDDE // 2) -40, (VINDU_HOYDE // 2)-40))
        vindu.blit(bilde, ((VINDU_BREDDE // 2)-140,VINDU_HOYDE //2))
        vindu.blit(bilde2, ((VINDU_BREDDE // 2) -150, (VINDU_HOYDE // 2 )+40))
    
    
    # Viser poeng
    score_text= font.render(str(score),True, (250,250,250))
    vindu.blit(score_text,(VINDU_BREDDE//2,(VINDU_HOYDE//2)-250))
    




    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()
