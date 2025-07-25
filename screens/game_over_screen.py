"""
Экран Game Over для Alien Invasion
"""

import pygame
import sys
import os
from button import Button


def game_over_screen(screen, stars, settings, level):
    """Экран окончания игры. Позволяет начать заново или выйти в меню."""
    base_folder = os.path.dirname(os.path.dirname(__file__))
    font_path = os.path.join(base_folder, "fonts&music", "retro_font.otf")
    title_font = pygame.font.Font(font_path, 200)
    game_over_surf = title_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_surf.get_rect(
        center=(settings.screen_width // 2, 150)
    )
    button_spacing = 40
    button_height = 120
    play_y = settings.screen_height // 2
    menu_y = play_y + button_height + button_spacing
    play_again_button = Button(
        screen,
        text="Play Again",
        center=(settings.screen_width // 2, play_y),
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
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif play_again_button.is_clicked(event):
                return "restart"
            elif menu_button.is_clicked(event):
                return "menu"
        stars.update()
        screen.fill(settings.bg_color)
        stars.draw(screen)
        screen.blit(game_over_surf, game_over_rect)
        play_again_button.draw()
        menu_button.draw()
        # Отображение уровня на экране Game Over (белый цвет)
        base_folder = os.path.dirname(os.path.dirname(__file__))
        retro_font_path = os.path.join(
            base_folder, "fonts&music", "retro_font.otf"
        )
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
