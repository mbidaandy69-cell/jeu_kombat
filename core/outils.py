import pygame

def decoupe_bande(chemin, nb_image, taille):
    bande= pygame.image.load(chemin).convert_alpha()
    largeur_image= bande.get_width() // nb_image
    images= []
    for i in range(nb_image):
        zone= pygame.Rect(i * largeur_image, 0, largeur_image, bande.get_height())
        image= pygame.Surface(zone.size, pygame.SRCALPHA)
        image.blit(bande, (0, 0), zone)
        images.append(pygame.transform.scale(image, taille))
    return images