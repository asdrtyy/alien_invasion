# Alien entity for Alien Invasion
from pygame.sprite import Sprite
import pygame
import os

class Alien(Sprite):
    """Класс пришельца."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        image_path = os.path.join(os.path.dirname(__file__), '../images/alien.bmp')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (120, 100))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.health = 1
        self.y = float(self.rect.y)  # Для плавного движения вниз
        self.random_move_started = False
        self.random_move_time = pygame.time.get_ticks()  # Без задержки, сразу
        self.random_dx = 0.0
        self.random_dy = 0.0
        self.last_random_update = pygame.time.get_ticks()
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    def update(self):
        pass  # Движение пришельцев теперь только через AlienInvasion._update_aliens
