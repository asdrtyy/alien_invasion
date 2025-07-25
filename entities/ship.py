# Ship entity for Alien Invasion
import pygame
import os

class Ship:
    """Класс для управления кораблем игрока."""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        image_path = os.path.join(os.path.dirname(__file__), '../images/ship.bmp')
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (180, 250))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 60
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.lives = 3
        # Анимация потери жизни
        self.is_animating = False
        self.animation_start_time = 0
        self.animation_duration = 800  # мс, длительность анимации
        self.animation_blink_interval = 100  # мс, интервал мигания

    def start_death_animation(self):
        """Запустить анимацию потери жизни."""
        self.is_animating = True
        self.animation_start_time = pygame.time.get_ticks()

    def update(self):
        if self.is_animating:
            now = pygame.time.get_ticks()
            if now - self.animation_start_time >= self.animation_duration:
                self.is_animating = False
                self.center_ship()  # вернуть в центр после анимации
            # Во время анимации не обновлять позицию по управлению
            return
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        if self.is_animating:
            # Мигание: показывать/скрывать корабль с интервалом
            now = pygame.time.get_ticks()
            if ((now - self.animation_start_time) // self.animation_blink_interval) % 2 == 0:
                self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
