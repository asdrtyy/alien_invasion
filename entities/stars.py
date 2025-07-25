# Star entity for Alien Invasion
import pygame
from pygame.sprite import Sprite
import random


class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.layer = random.choices([1, 2, 3], weights=[2, 3, 1])[0]
        if self.layer == 1:
            self.size = random.randint(1, 2)
            self.speed = 0.1
            self.base_brightness = 60
        elif self.layer == 2:
            self.size = random.randint(2, 4)
            self.speed = 0.3
            self.base_brightness = 130
        else:
            self.size = random.randint(3, 5)
            self.speed = 0.6
            self.base_brightness = 220
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.brightness = self.base_brightness
        self.update_color()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen_rect.width)
        self.rect.y = random.randint(0, self.screen_rect.height)

    def update_color(self):
        color = (int(self.brightness),) * 3
        self.image.fill(color)

    def update(self):
        self.brightness += getattr(self, "pulse_direction", 1) * getattr(
            self, "pulse_speed", 0.5
        )
        if (
            self.brightness >= 255
            or self.brightness <= self.base_brightness - 30
        ):
            self.pulse_direction = -getattr(self, "pulse_direction", 1)
        self.brightness = max(0, min(255, self.brightness))
        self.update_color()
        self.rect.y += self.speed
        if self.rect.top > self.screen_rect.height:
            self.rect.y = -self.size
            self.rect.x = random.randint(0, self.screen_rect.width)
