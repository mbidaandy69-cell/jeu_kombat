import pygame
from settings import *
import os
from core.outils import decoupe_bande

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
        dossier= os.path.join(os.path.dirname(__file__), "..", "assets", "images", "samurai")
        self.images_repos= decoupe_bande(os.path.join(dossier, "idle1.png"), 10, (240, 240))
        self.index_image= 0
        self.compteur_anim= 0
        self.images_course= decoupe_bande(os.path.join(dossier, "run1.png"), 16, (240, 240))
        self.image_attaque= decoupe_bande(os.path.join(dossier, "attaque1.png"), 7, (240, 240))
        self.touche_timer= 0
        self.imagr_touche= decoupe_bande(os.path.join(dossier, "hurt1.png"), 4, (240, 240))
        self.animation= {"repos": self.images_repos, "course": self.images_course, "attaque": self.image_attaque, "touche": self.imagr_touche, "ko": [pygame.transform.rotate(self.imagr_touche[-1], 90)]}
        self.etat_anim= "repos"
        self.en_mouvement= False
        self.image_ko= [pygame.transform.rotate(self.imagr_touche[-1], 90)]

    def move(self, dx=0, dy=0):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, surface):
        image= self.animation[self.etat_anim][self.index_image]
        if not self.regarde_droite:
            image= pygame.transform.flip(image, True, False)
        rect_image= image.get_rect(midbottom= self.rect.midbottom)
        rect_image.y+= DECALAGE_Y
        if self.etat_anim== "ko":
            rect_image.y+= DECALAGE_KO
        surface.blit(image, rect_image)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Draw the fighter's rectangle
        zone= self.zone_attaque()
        if zone:
            pygame.draw.rect(surface, (255, 255, 0), zone, 2)  # Draw the attack zone in yellow
        for i, img in enumerate(self.animation["attaque"]):
            (pygame.transform.scale(img, (96, 96)), (10 + i * 100, 120))
        
    def deplacer(self, touch_left, touch_right, touches):
        self.en_mouvement= False
        if self.touche_timer > 0:
            return  # Skip movement if the fighter is in a hit state
        if touches[touch_left]:
            self.rect.x -= VITESSE
            self.en_mouvement= True
        if touches[touch_right]:
            self.rect.x += VITESSE
            self.en_mouvement= True
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
        if touche[touche_attaque] and self.attaque_time== 0 and self.touche_timer== 0:
            self.attaque_time= DUREE_ATTAQUE
            self.a_touche= False
            
    def zone_attaque(self):
        if self.attaque_time== 0:
            return None
        
        total= len(self.animation["attaque"])
        image_actuelle= (DUREE_ATTAQUE - self.attaque_time) * total // DUREE_ATTAQUE
        if image_actuelle < IMAGE_DEBUT_COUP:
            return None
        
        if self.regarde_droite:
            return pygame.Rect(self.rect.right, self.rect.y +40, 70, 40)
        return pygame.Rect(self.rect.left - 70, self.rect.y +40, 70, 40)
    
    def mettre_a_jour_attaque(self):
            if self.attaque_time > 0:
                self.attaque_time-= 1
            
            if self.touche_timer > 0:
                self.touche_timer -= 1
                
    def toucher(self, adversaire):
        zone= self.zone_attaque()
        if  zone and not self.a_touche and zone.colliderect(adversaire.rect):
            adversaire.health= max(0, adversaire.health - DEGATS)
            self.a_touche= True
            adversaire.touche_timer= DUREE_TOUCHE
            adversaire.attaque_time= 0  # Stop the opponent's attack if they are hit
            
    def animer(self):
        if self.health <= 0:
            nouvelle_etat = "ko"
        elif self.touche_timer > 0:
            nouvelle_etat = "touche"    
        elif self.touche_timer > 0:
            nouvelle_etat = "touche"
        elif self.attaque_time > 0:
            nouvelle_etat = "attaque"
        elif self.en_mouvement:
            nouvelle_etat = "course"
        else:
            nouvelle_etat = "repos"
        if nouvelle_etat != self.etat_anim:
            self.etat_anim = nouvelle_etat
            self.index_image = 0
            self.compteur_anim = 0
        if self.etat_anim == "attaque":
            total = len(self.animation["attaque"])
            self.index_image = min(total - 1, (DUREE_ATTAQUE - self.attaque_time) * total // DUREE_ATTAQUE)
            return
        self.compteur_anim += 1
        if self.compteur_anim >= VITESSE_ANIM:
            self.compteur_anim = 0
            self.index_image = (self.index_image + 1) % len(self.animation[self.etat_anim])