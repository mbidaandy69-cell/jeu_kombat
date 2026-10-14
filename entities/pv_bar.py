#coding: utf-8

import pygame

class PVBar(pygame.sprite.Sprite):
    def __init__(self, pv, max_pv, width=100, height=10):
        super().__init__()
        self.pv = pv
        self.max_pv = max_pv
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_bar()

    def update_bar(self):
        # Calculate the percentage of health remaining
        health_percentage = self.pv / self.max_pv
        # Calculate the width of the health bar based on the percentage
        current_width = int(self.width * health_percentage)
        
        # Fill the background with red (representing lost health)
        self.image.fill((255, 0, 0))
        
        # Draw the current health in green
        if current_width > 0:
            pygame.draw.rect(self.image, (0, 255, 0), (0, 0, current_width, self.height))

    def set_pv(self, new_pv):
        self.pv = max(0, min(new_pv, self.max_pv))  # Ensure pv is within bounds
        self.update_bar()