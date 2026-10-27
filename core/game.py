#coding: utf-8
import pygame
import os
from settings import *
from entities.fighter import Fighter
from entities.pv_bar import PVBar
from entities.personnages import PERSONNAGES
from core.outils import decoupe_bande

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
        self.police_info = pygame.font.Font(None, 28)
        self.cles = list(PERSONNAGES)
        self.choix = [0, 1]
        self.valide = [False, False]
        self.apercus = {}
        for cle in self.cles:
            fiche = PERSONNAGES[cle]
            fichier, nombre = fiche["animations"]["repos"]
            chemin = os.path.join(os.path.dirname(__file__), "..", "assets", "images", fiche["dossier"], fichier)
            self.apercus[cle] = decoupe_bande(chemin, nombre, TAILLE_IMAGE)[0]
        self.nouvelle_partie()

    def gerer_evenements(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if self.etat == "menu" and event.key == pygame.K_RETURN:
                        self.ouvrir_choix()
                    elif self.etat == "choix":
                        self.gerer_choix(event.key)
                    elif self.etat == "combat" and self.vainqueur and event.key == pygame.K_RETURN:
                        if self.score1 == MANCHES_VICTOIRE or self.score2 == MANCHES_VICTOIRE:
                            self.score1 = 0
                            self.score2 = 0
                            self.ouvrir_choix()
                        else:
                            self.nouvelle_partie()

    def ouvrir_choix(self):
        self.etat = "choix"
        self.choix = [0, 1]
        self.valide = [False, False]

    def gerer_choix(self, touche):
        n = len(self.cles)
        commandes = [(pygame.K_q, pygame.K_d, pygame.K_l),
                     (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_v)]
        for joueur, (gauche, droite, valider) in enumerate(commandes):
            if self.valide[joueur]:
                continue
            if touche == gauche:
                self.choix[joueur] = (self.choix[joueur] - 1) % n
            elif touche == droite:
                self.choix[joueur] = (self.choix[joueur] + 1) % n
            elif touche == valider:
                self.valide[joueur] = True
        if all(self.valide):
            self.nouvelle_partie()
            self.etat = "combat"

    def draw(self):
        if self.etat== "menu":
            self.screen.fill(COULEUR_FOND)
            titre = self.police.render("last kombat", True, (255, 255, 255))
            self.screen.blit(titre, titre.get_rect(center=(LARGEUR_FENETRE // 2, 200)))
            consigne= self.petite_police.render("appuyer sur entre pour commencer", True, (255, 255, 255))
            self.screen.blit(consigne, consigne.get_rect(center=(LARGEUR_FENETRE // 2, 350)))
            pygame.display.flip()
            return
        
        if self.etat== "choix":
            self.dessiner_choix()
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
        self.player1= Fighter(250, SOL_Y, self.cles[self.choix[0]])
        self.player2= Fighter(750, SOL_Y, self.cles[self.choix[1]])
        self.player1_pv_bar = PVBar(self.player1.health, self.player1.max_health, 400, 25)
        self.player2_pv_bar = PVBar(self.player2.health, self.player2.max_health, 400, 25)  
        self.vainqueur = None  # Initialize the winner attribute
        self.temps_restant= DUREE_MANCHE * FPS  # Initialize the remaining time for the round
        
        
    def run(self):
        while self.running:
            self.gerer_evenements()
            self.mettre_à_jour()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        
    def mettre_à_jour(self):
        if self.etat!= "combat":
            return
        if self.vainqueur:
            self.player1.animer()
            self.player2.animer()
            return
        
        touches= pygame.key.get_pressed()
        self.player1.deplacer(pygame.K_q, pygame.K_d, touches)
        self.player2.deplacer(pygame.K_LEFT, pygame.K_RIGHT, touches)
        self.player1.sauter(pygame.K_z , touches)
        self.player2.sauter(pygame.K_UP, touches)
        self.player1.appliquer_gravite()
        self.player2.appliquer_gravite()
        self.player1.repousser(self.player2)
        self.player1.faire_face(self.player2)
        self.player2.faire_face(self.player1)
        self.player1.attaquer(pygame.K_l, touches)
        self.player2.attaquer(pygame.K_v, touches)
        self.player1.toucher(self.player2)
        self.player2.toucher(self.player1)
        self.player1.mettre_a_jour_attaque()
        self.player2.mettre_a_jour_attaque()
        self.player1.animer()
        self.player2.animer()
        self.player1_pv_bar.set_pv(self.player1.health)
        self.player2_pv_bar.set_pv(self.player2.health)   
        if self.player1.health <= 0:
            self.vainqueur = "Joueur 2"
            self.score2 += 1
        elif self.player2.health <= 0:
            self.vainqueur = "Joueur 1"
            self.score1 += 1
        
    def dessiner_choix(self):
        self.screen.fill(COULEUR_FOND)
        titre = self.petite_police.render("Choisissez votre combattant", True, (255, 255, 255))
        self.screen.blit(titre, titre.get_rect(center=(LARGEUR_FENETRE // 2, 40)))
        largeur_case = LARGEUR_FENETRE // len(self.cles)
        for i, cle in enumerate(self.cles):
            fiche = PERSONNAGES[cle]
            centre_x = largeur_case * i + largeur_case // 2
            image = pygame.transform.scale(self.apercus[cle], (264, 216))
            self.screen.blit(image, image.get_rect(center=(centre_x, 250)))
            nom = self.petite_police.render(fiche["nom"], True, (255, 255, 255))
            self.screen.blit(nom, nom.get_rect(center=(centre_x, 380)))
            
        couleurs = [(0, 120, 255), (220, 40, 40)]
        for joueur in range(2):
            centre_x = largeur_case * self.choix[joueur] + largeur_case // 2
            cadre = pygame.Rect(0, 0, largeur_case - 20 - 16 * joueur, 340 - 16 * joueur)
            cadre.center = (centre_x, 270)
            epaisseur = 6 if self.valide[joueur] else 2
            pygame.draw.rect(self.screen, couleurs[joueur], cadre, epaisseur)
            etiquette = f"J{joueur + 1} pret" if self.valide[joueur] else f"J{joueur + 1}"
            texte = self.police_info.render(etiquette, True, couleurs[joueur])
            self.screen.blit(texte, texte.get_rect(center=(centre_x - 50 + 100 * joueur, 450)))
        aide1 = self.police_info.render("J1 : Q D pour choisir, L pour valider", True, (200, 200, 200))
        aide2 = self.police_info.render("J2 : fleches pour choisir, V pour valider", True, (200, 200, 200))
        self.screen.blit(aide1, aide1.get_rect(center=(LARGEUR_FENETRE // 2, 530)))
        self.screen.blit(aide2, aide2.get_rect(center=(LARGEUR_FENETRE // 2, 560)))
        pygame.display.flip()