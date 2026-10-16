import pygame
from settings import *
from entities.fighter import Fighter
from entities.pv_bar import PVBar

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
        pygame.display.set_caption(TITRE_FENETRE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.police = pygame.font.Font(None, 90)  # Default font and size for displaying text
        self.score1= 0
        self.score2= 0
        self.petite_police = pygame.font.Font(None, 50)  # Smaller font for displaying scores
        self.etat= "menu"
        self.nouvelle_partie()

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.vainqueur:
                if self.score1== MANCHES_VICTOIRE or self.score2== MANCHES_VICTOIRE:
                    self.score1= 0
                    self.score2= 0
                self.nouvelle_partie()
                
            if event.type== pygame.KEYDOWN and event.key == pygame.K_RETURN and self.etat== "menu":
                self.etat= "combat"

    def draw(self):
        if self.etat== "menu":
            self.screen.fill(COULEUR_FOND)
            titre = self.police.render("last kombat", True, (255, 255, 255))
            self.screen.blit(titre, titre.get_rect(center=(LARGEUR_FENETRE // 2, 200)))
            consigne= self.petite_police.render("appuyer sur entre pour commencer", True, (255, 255, 255))
            self.screen.blit(consigne, consigne.get_rect(center=(LARGEUR_FENETRE // 2, 350)))
            pygame.display.flip()
            return
        self.screen.fill(COULEUR_FOND)
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.screen.blit(self.player1_pv_bar.image, (10, 10))
        self.screen.blit(self.player2_pv_bar.image, (LARGEUR_FENETRE - self.player2_pv_bar.width - 10, 10))
        if self.vainqueur:
            if self.score1== MANCHES_VICTOIRE or self.score2== MANCHES_VICTOIRE:
                message= f"{self.vainqueur} gagne le match "
            else:
                message= f"{self.vainqueur} gagne la manche "   
            texte_vainqueur = self.police.render(message, True, (255, 255, 255))
            
            texte_rect = texte_vainqueur.get_rect(center=(LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2))
            self.screen.blit(texte_vainqueur, texte_rect)
        score= self.petite_police.render(f"{self.score1}-{self.score2}", True, (255, 255, 255) )
        self.screen.blit(score, score.get_rect(center= (LARGEUR_FENETRE // 2, 25)))
        pygame.display.flip()
    
    def nouvelle_partie(self):
        self.player1= Fighter(200, 350, 50, 100, (0, 120, 255))
        self.player2= Fighter(720, 350, 50, 100, (220, 40, 40))
        self.player1_pv_bar = PVBar(self.player1.health, self.player1.max_health, 400, 25)
        self.player2_pv_bar = PVBar(self.player2.health, self.player2.max_health, 400, 25)  
        self.vainqueur = None  # Initialize the winner attribute
        
        
    def run(self):
        while self.running:
            self.gerer_evenements()
            self.mettre_à_jour()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        
    def mettre_à_jour(self):
        if self.etat== "menu" or self.vainqueur:
            return
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
        self.player1.mettre_a_jour_attaque()
        self.player2.mettre_a_jour_attaque()
        self.player1_pv_bar.set_pv(self.player1.health)
        self.player2_pv_bar.set_pv(self.player2.health)   
        if self.player1.health <= 0:
            self.vainqueur = "Joueur 2"
            self.score2 += 1
        elif self.player2.health <= 0:
            self.vainqueur = "Joueur 1"
            self.score1 += 1
        