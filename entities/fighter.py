#coding: utf-8

import os
import pygame
from settings import *
from core.outils import decoupe_bande
from entities.personnages import PERSONNAGES

ECRAN = pygame.Rect(0, 0, LARGEUR_FENETRE, HAUTEUR_FENETRE)


class Fighter:
    def __init__(self, x, y, cle):
        self.fiche = PERSONNAGES[cle]
        largeur, hauteur = self.fiche["boite"]
        self.rect = pygame.Rect(0, 0, largeur, hauteur)
        self.rect.midbottom = (x, y)

        self.health = self.fiche["vie"]
        self.max_health = self.fiche["vie"]
        self.vitesse = self.fiche["vitesse"]
        self.force_saut = self.fiche["force_saut"]

        self.vitesse_y = 0
        self.sur_sol = True
        self.regarde_droite = True
        self.en_mouvement = False
        self.recule = False
        self.touche_timer = 0

        self.numero_coup = 0
        self.attaque_time = 0
        self.fenetre = 0
        self.suite = False
        self.a_touche = False
        self.touche_avant = False

        self.etat_anim = "repos"
        self.index_image = 0
        self.compteur_anim = 0
        self.charger_images()

    def charger_images(self):
        dossier = os.path.join(os.path.dirname(__file__), "..", "assets", "images", self.fiche["dossier"])
        self.animation = {}
        for nom, (fichier, nombre) in self.fiche["animations"].items():
            self.animation[nom] = decoupe_bande(os.path.join(dossier, fichier), nombre, TAILLE_IMAGE)
        self.animation_coups = []
        for coup in self.fiche["coups"]:
            chemin = os.path.join(dossier, coup["image"])
            self.animation_coups.append(decoupe_bande(chemin, coup["nb_images"], TAILLE_IMAGE))
            
    def draw(self, surface):
        if self.etat_anim == "attaque":
            image = self.animation_coups[self.numero_coup][self.index_image]
        else:
            image = self.animation[self.etat_anim][self.index_image]
        if not self.regarde_droite:
            image = pygame.transform.flip(image, True, False)
        place = image.get_rect(midbottom=self.rect.midbottom)
        place.y += MARGE_SOL
        surface.blit(image, place)
        if AFFICHER_BOITES:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
            zone = self.zone_attaque()
            if zone:
                pygame.draw.rect(surface, (255, 255, 0), zone, 2)

    def deplacer(self, touche_gauche, touche_droite, touches):
        self.en_mouvement = False
        self.recule = False
        if self.touche_timer > 0 or self.attaque_time > 0 or self.health <= 0:
            return
        direction = 0
        if touches[touche_gauche]:
            direction -= 1
        if touches[touche_droite]:
            direction += 1
        if direction == 0:
            return
        self.en_mouvement = True
        vers_adversaire = (direction == 1) == self.regarde_droite
        self.recule = not vers_adversaire
        vitesse = self.vitesse * 0.7 if self.recule else self.vitesse
        self.rect.x += direction * round(vitesse)
        self.rect.clamp_ip(ECRAN)

    def sauter(self, touche_saut, touches):
        libre = self.attaque_time == 0 and self.touche_timer == 0 and self.health > 0
        if touches[touche_saut] and self.sur_sol and libre:
            self.vitesse_y = -self.force_saut
            self.sur_sol = False

    def appliquer_gravite(self):
        self.vitesse_y += GRAVITE
        self.rect.y += self.vitesse_y
        if self.rect.bottom >= SOL_Y:
            self.rect.bottom = SOL_Y
            self.vitesse_y = 0
            self.sur_sol = True

    def faire_face(self, adversaire):
        self.regarde_droite = self.rect.centerx < adversaire.rect.centerx
        
    def attaquer(self, touche_attaque, touches):
        enfoncee = touches[touche_attaque]
        nouvel_appui = enfoncee and not self.touche_avant
        self.touche_avant = enfoncee
        if not nouvel_appui or self.touche_timer > 0 or self.health <= 0:
            return
        dernier = len(self.fiche["coups"]) - 1
        if self.attaque_time > 0:
            if self.numero_coup < dernier:
                self.suite = True
        elif self.fenetre > 0 and self.numero_coup < dernier:
            self.lancer_coup(self.numero_coup + 1)
        else:
            self.lancer_coup(0)

    def lancer_coup(self, numero):
        self.numero_coup = numero
        self.attaque_time = self.fiche["coups"][numero]["duree"]
        self.a_touche = False
        self.suite = False
        self.fenetre = 0

    def zone_attaque(self):
        if self.attaque_time == 0:
            return None
        coup = self.fiche["coups"][self.numero_coup]
        total = coup["nb_images"]
        image_actuelle = (coup["duree"] - self.attaque_time) * total // coup["duree"]
        debut, fin = coup["actif"]
        if not (debut <= image_actuelle <= fin):
            return None
        haut = self.rect.y + int(self.rect.height * 0.25)
        hauteur = int(self.rect.height * 0.3)
        if self.regarde_droite:
            return pygame.Rect(self.rect.right, haut, coup["portee"], hauteur)
        return pygame.Rect(self.rect.left - coup["portee"], haut, coup["portee"], hauteur)

    def toucher(self, adversaire):
        zone = self.zone_attaque()
        if zone and not self.a_touche and adversaire.health > 0 and zone.colliderect(adversaire.rect):
            coup = self.fiche["coups"][self.numero_coup]
            adversaire.health = max(0, adversaire.health - coup["degats"])
            self.a_touche = True
            adversaire.touche_timer = DUREE_TOUCHE
            adversaire.attaque_time = 0
            adversaire.suite = False
            adversaire.fenetre = 0
            direction = 1 if self.regarde_droite else -1
            adversaire.rect.x += direction * 12
            adversaire.rect.clamp_ip(ECRAN)

    def mettre_a_jour_attaque(self):
        if self.touche_timer > 0:
            self.touche_timer -= 1
        if self.attaque_time > 0:
            self.attaque_time -= 1
            if self.attaque_time == 0:
                if self.suite:
                    self.lancer_coup(self.numero_coup + 1)
                else:
                    self.fenetre = FENETRE_COMBO
        elif self.fenetre > 0:
            self.fenetre -= 1
            if self.fenetre == 0:
                self.numero_coup = 0
    
    def animer(self):
        if self.health <= 0:
            nouvel_etat = "ko"
        elif self.touche_timer > 0:
            nouvel_etat = "touche"
        elif self.attaque_time > 0:
            nouvel_etat = "attaque"
        elif not self.sur_sol:
            nouvel_etat = "saut"
        elif self.en_mouvement:
            nouvel_etat = "marche"
        else:
            nouvel_etat = "repos"
        if nouvel_etat != self.etat_anim:
            self.etat_anim = nouvel_etat
            self.index_image = 0
            self.compteur_anim = 0

        if self.etat_anim == "attaque":
            coup = self.fiche["coups"][self.numero_coup]
            total = coup["nb_images"]
            self.index_image = min(total - 1, (coup["duree"] - self.attaque_time) * total // coup["duree"])
            return
        if self.etat_anim == "saut":
            if self.vitesse_y < -4:
                self.index_image = 0
            elif self.vitesse_y <= 4:
                self.index_image = 1
            else:
                self.index_image = 2
            return

        self.compteur_anim += 1
        if self.etat_anim == "marche":
            duree = max(1, round(18 / self.vitesse))
        else:
            duree = ANIM_TICKS[self.etat_anim]
        if self.compteur_anim >= duree:
            self.compteur_anim = 0
            total = len(self.animation[self.etat_anim])
            if self.etat_anim in ("ko", "touche"):
                self.index_image = min(self.index_image + 1, total - 1)
            elif self.etat_anim == "marche" and self.recule:
                self.index_image = (self.index_image - 1) % total
            else:
                self.index_image = (self.index_image + 1) % total
                
    def repousser(self, autre):
        if not self.rect.colliderect(autre.rect):
            return
        chevauche = min(self.rect.right, autre.rect.right) - max(self.rect.left, autre.rect.left)
        moitie = chevauche // 2 + 1
        if self.rect.centerx < autre.rect.centerx:
            self.rect.x -= moitie
            autre.rect.x += moitie
        else:
            self.rect.x += moitie
            autre.rect.x -= moitie
        self.rect.clamp_ip(ECRAN)
        autre.rect.clamp_ip(ECRAN)