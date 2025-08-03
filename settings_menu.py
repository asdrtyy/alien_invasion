"""Модуль меню настроек для Alien Invasion."""

import pygame
import sys
import os
from button import Button
from settings import Settings


def settings_menu(settings):
    
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height)
    )
    pygame.display.set_caption("Settings")
    clock = pygame.time.Clock()
    base_folder = os.path.dirname(__file__)
    font_path = os.path.join(base_folder, "fonts&music", "retro_font.otf")
    font = pygame.font.Font(font_path, 60)
    title = font.render("SETTINGS", True, (255, 255, 255))
    title_rect = title.get_rect(center=(settings.screen_width // 2, 120))
    # Пример: настройка количества жизней
    lives = settings.lives if hasattr(settings, "lives") else 3
    lives_btn = Button(
        screen,
        text=f"Lives: {lives}",
        center=(settings.screen_width // 2, 300),
        width=400,
        height=80,
        font_path=font_path,
        font_size=40,
    )
    save_btn = Button(
        screen,
        text="Save & Return",
        center=(settings.screen_width // 2, 500),
        width=400,
        height=80,
        font_path=font_path,
        font_size=40,
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if lives_btn.is_clicked(event):
                lives = 1 if lives >= 5 else lives + 1
                lives_btn.text = f"Lives: {lives}"
                lives_btn.text_surf = lives_btn.font.render(
                    lives_btn.text, True, lives_btn.text_color
                )
                lives_btn.text_rect = lives_btn.text_surf.get_rect(
                    center=lives_btn.rect.center
                )
            if save_btn.is_clicked(event):
                settings.lives = lives
                return
        screen.fill(settings.bg_color)
        screen.blit(title, title_rect)
        lives_btn.draw()
        save_btn.draw()
        pygame.display.flip()
        clock.tick(60)
