"""Модуль кнопок для Alien Invasion."""

import os
import pygame


class Button:
    """Класс для кнопки интерфейса."""

    def __init__(
        self,
        screen,
        text,
        center,
        width=500,
        height=120,
        font_path=None,
        font_size=40,
        bg_color=(32, 32, 32),
        hover_color=(64, 64, 64),
        text_color=(255, 255, 255),
        border_radius=12,
    ):
        self.screen = screen
        self.text = text
        self.center = center
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.center

        if font_path is None:
            self.font = pygame.font.SysFont(None, font_size)
        else:
            # Если путь абсолютный — используем как есть, иначе ищем относительно корня проекта
            if os.path.isabs(font_path):
                font_full_path = font_path
            else:
                # Корень проекта — папка alien_invasion (где лежит button.py)
                project_root = os.path.dirname(__file__)
                font_full_path = os.path.join(project_root, font_path)
            self.font = pygame.font.Font(font_full_path, font_size)

        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        """Рисует кнопку на экране."""
        mouse_pos = pygame.mouse.get_pos()
        color = (
            self.hover_color
            if self.rect.collidepoint(mouse_pos)
            else self.bg_color
        )
        pygame.draw.rect(
            self.screen, color, self.rect, border_radius=self.border_radius
        )
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.rect,
            2,
            border_radius=self.border_radius,
        )
        self.screen.blit(self.text_surf, self.text_rect)
        
    def is_clicked(self, event):
        clicked = (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
        if clicked:
            print(f"Button '{self.text}' clicked!")
        return clicked