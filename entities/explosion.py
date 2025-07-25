# Explosion entity for Alien Invasion
import pygame
from pygame.sprite import Sprite
import os


class Explosion(Sprite):
    def __init__(self, position, size=(120, 100), duration=400):
        super().__init__()
        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(
            base_folder, "../images/EXPLOSION_ANIMATION.png"
        )
        sprite_sheet = pygame.image.load(image_path).convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()
        frame_count = 6
        frame_width = sheet_width // frame_count
        frame_height = sheet_height
        self.frames = []
        for i in range(frame_count):
            frame = sprite_sheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height)
            ).copy()
            frame = pygame.transform.scale(frame, size)
            self.frames.append(frame)
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=position)

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        frame = int((elapsed / self.duration) * len(self.frames))
        if frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[frame]
