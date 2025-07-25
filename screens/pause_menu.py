"""
Экран паузы для Alien Invasion
"""

import pygame
import sys
import os
from button import Button


def pause_menu(screen, stars, settings, level):
    import builtins

    if not hasattr(builtins, "SOUND_ENABLED"):
        builtins.SOUND_ENABLED = True
    # --- Музыкальная кнопка ---
    music_btn_size = 48
    music_on_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../images/music_on.png")
    ).convert_alpha()
    music_off_img = pygame.image.load(
        os.path.join(os.path.dirname(__file__), "../images/music_off.png")
    ).convert_alpha()
    music_on_img = pygame.transform.smoothscale(
        music_on_img, (music_btn_size, music_btn_size)
    )
    music_off_img = pygame.transform.smoothscale(
        music_off_img, (music_btn_size, music_btn_size)
    )
    music_btn_rect = music_on_img.get_rect(topleft=(10, 10))
    music_playing = [
        pygame.mixer.music.get_busy() and not pygame.mixer.music.get_pos() == -1
    ]
    sound_enabled = [builtins.SOUND_ENABLED]
    # --- Синхронизация состояния кнопки с глобальным SOUND_ENABLED ---
    if hasattr(builtins, "SOUND_ENABLED"):
        sound_enabled[0] = bool(builtins.SOUND_ENABLED)
        music_playing[0] = bool(builtins.SOUND_ENABLED)
    else:
        sound_enabled[0] = True
        music_playing[0] = True
    """Меню паузы. Позволяет продолжить игру или выйти в меню."""
    base_folder = os.path.dirname(os.path.dirname(__file__))
    font_path = os.path.join(base_folder, "fonts&music", "retro_font.otf")
    button_height = 120
    button_spacing = 40
    continue_y = settings.screen_height // 2
    menu_y = continue_y + button_height + button_spacing
    continue_button = Button(
        screen,
        text="Continue",
        center=(settings.screen_width // 2, continue_y),
        font_path=font_path,
        font_size=50,
        height=button_height,
    )
    menu_button = Button(
        screen,
        text="Return to Menu",
        center=(settings.screen_width // 2, menu_y),
        font_path=font_path,
        font_size=50,
        height=button_height,
        bg_color=(32, 32, 32),
        hover_color=(64, 64, 64),
    )
    title_font = pygame.font.Font(font_path, 120)
    title_surf = title_font.render("PAUSED", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(settings.screen_width // 2, 150))
    clock = pygame.time.Clock()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif continue_button.is_clicked(event):
                paused = False
            elif menu_button.is_clicked(event):
                return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if music_btn_rect.collidepoint(event.pos):
                    if music_playing[0]:
                        pygame.mixer.music.pause()
                        music_playing[0] = False
                        sound_enabled[0] = False
                    else:
                        pygame.mixer.music.unpause()
                        music_playing[0] = True
                        sound_enabled[0] = True
        stars.update()
        screen.fill(settings.bg_color)
        stars.draw(screen)
        screen.blit(title_surf, title_rect)
        continue_button.draw()
        menu_button.draw()
        # Кнопка музыки
        if music_playing[0]:
            screen.blit(music_on_img, (music_btn_rect.x, music_btn_rect.y))
        else:
            screen.blit(music_off_img, (music_btn_rect.x, music_btn_rect.y))
        builtins.SOUND_ENABLED = sound_enabled[0]
        # Корректное отображение уровня в меню паузы (белый цвет)
        base_folder = os.path.dirname(os.path.dirname(__file__))
        retro_font_path = os.path.join(base_folder, "fonts&music", "retro_font.otf")
        font = pygame.font.Font(retro_font_path, 48)
        level_surf = font.render(f"Level: {level}", True, (255, 255, 255))
        level_rect = level_surf.get_rect(
            bottomright=(
                settings.screen_width - 20,
                settings.screen_height - 20,
            )
        )
        screen.blit(level_surf, level_rect)
        pygame.display.flip()
        clock.tick(60)
    return None
