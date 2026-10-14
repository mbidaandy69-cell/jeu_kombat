import pygame
from settings import *

class Fighter:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = 100
        self.speed = 5
        self.vitesse_y= 0
        self.sur_sol = False
        self.regarde_droite= True
        self.attaque_time= 0
        self.a_touche= False
        self.max_health = 100  # Assuming max health is 100
        self.vainqueur = None  # Initialize the winner attribute
        self.police = pygame.font.Font(None, 90)  # Default font and size for displaying text

    def move(self, dx=0, dy=0):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        zone= self.zone_attaque()
        if zone:
            pygame.draw.rect(surface, (255, 255, 0), zone)
        
    def deplacer(self, touch_left, touch_right, touches):
        if touches[touch_left]:
            self.rect.x -= VITESSE
        if touches[touch_right]:
            self.rect.x += VITESSE
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > LARGEUR_FENETRE:
            self.rect.right = LARGEUR_FENETRE
            
    def sauter(self, touche_saut, touches):
        if touches[touche_saut] and self.sur_sol:
            self.vitesse_y = -FORCE_SAUT
            self.sur_sol = False
            
    def appliquer_gravite(self):
        self.vitesse_y += GRAVITE
        self.rect.y += self.vitesse_y
        if self.rect.bottom >= SOL_Y:
            self.rect.bottom = SOL_Y
            self.vitesse_y = 0
            self.sur_sol = True
    
    def faire_face(self, adversaire):
        self.regarde_droite= self.rect.centerx < adversaire.rect.centerx
        
    def attaquer(self, touche_attaque, touche):
        if touche[touche_attaque] and self.attaque_time== 0:
            self.attaque_time= DUREE_ATTAQUE
            self.a_touche= False
            
    def zone_attaque(self):
        if self.attaque_time== 0:
            return None

        if self.regarde_droite:
            return pygame.Rect(self.rect.right, self.rect.y +40, 70, 40)
        return pygame.Rect(self.rect.left - 70, self.rect.y +40, 70, 40)
    
    def mettre_a_jour_attaque(self):
            if self.attaque_time > 0:
                self.attaque_time-= 1
                
    def toucher(self, adversaire):
        zone= self.zone_attaque()
        if  zone and not self.a_touche and zone.colliderect(adversaire.rect):
            adversaire.health= max(0, adversaire.health - DEGATS)
            self.a_touche= True
                
    