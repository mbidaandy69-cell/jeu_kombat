import pygame
from settings import *
from entities.fighter import Fighter

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
        pygame.display.set_caption(TITRE_FENETRE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player1= Fighter(200, 350, 50, 100, (0, 120, 255))
        self.player2= Fighter(720, 350, 50, 100, (220, 40, 40))

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def draw(self):
        self.screen.fill(COULEUR_FOND)
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.gerer_evenements()
            self.mettre_à_jour()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        
    def mettre_à_jour(self):
        touches= pygame.key.get_pressed()
        self.player1.deplacer(pygame.K_q, pygame.K_d, touches)
        self.player2.deplacer(pygame.K_LEFT, pygame.K_RIGHT, touches)
        self.player1.sauter(pygame.K_z , touches)
        self.player2.sauter(pygame.K_UP, touches)
        self.player1.appliquer_gravite()
        self.player2.appliquer_gravite()
        self.player1.faire_face(self.player2)
        self.player2.faire_face(self.player1)
        self.player1.attaquer(pygame.K_l, touches)
        self.player2.attaquer(pygame.K_v, touches)
        self.player1.toucher(self.player2)
        self.player2.toucher(self.player1)
        print(self.player1.health, self.player2.health)
        self.player1.mettre_a_jour_attaque()
        self.player2.mettre_a_jour_attaque()
        