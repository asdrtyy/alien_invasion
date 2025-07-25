"""
Экран завершения уровня для Alien Invasion
"""
import pygame
import sys
import os
from button import Button

def level_complete_screen(screen, stars, settings, level, is_last_level=False):
    """Экран завершения уровня. Позволяет продолжить или выйти в меню, на последнем уровне — поздравление."""
    base_folder = os.path.dirname(os.path.dirname(__file__))
    font_path = os.path.join(base_folder, 'fonts&music', 'retro_font.otf')
    title_font = pygame.font.Font(font_path, 120)
    if is_last_level:
        title_text = f"Level {level} Complete!"
        congrats_text = "Congratulations! Game completed!"
    else:
        title_text = f"Level {level} Complete!"
        congrats_text = ""
    title_surf = title_font.render(title_text, True, (0, 255, 0))
    title_rect = title_surf.get_rect(center=(settings.screen_width // 2, 200))
    if congrats_text:
        congrats_font = pygame.font.Font(font_path, 70)
        congrats_surf = congrats_font.render(congrats_text, True, (255, 255, 0))
        congrats_rect = congrats_surf.get_rect(center=(settings.screen_width // 2, 350))
    button_height = 120
    button_spacing = 40
    continue_y = settings.screen_height // 2 + 100
    menu_y = continue_y + button_height + button_spacing
    continue_button = Button(
        screen,
        text="Continue",
        center=(settings.screen_width // 2, continue_y),
        font_path=font_path,
        font_size=50,
        height=button_height
    )
    menu_button = Button(
        screen,
        text="Menu",
        center=(settings.screen_width // 2, menu_y),
        font_path=font_path,
        font_size=50,
        height=button_height,
        bg_color=(32, 32, 32),
        hover_color=(64, 64, 64)
    )
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not is_last_level and continue_button.is_clicked(event):
                return 'continue'
            if menu_button.is_clicked(event):
                return 'menu'
        stars.update()
        screen.fill(settings.bg_color)
        stars.draw(screen)
        screen.blit(title_surf, title_rect)
        if congrats_text:
            screen.blit(congrats_surf, congrats_rect)
        if not is_last_level:
            continue_button.draw()
        menu_button.draw()
        # Level внизу экрана — тем же ретро-шрифтом
        retro_font_path = os.path.join(base_folder, 'fonts&music', 'retro_font.otf')
        font = pygame.font.Font(retro_font_path, 48)
        level_surf = font.render(f"Level: {level}", True, (255, 255, 255))
        level_rect = level_surf.get_rect(bottomright=(settings.screen_width - 20, settings.screen_height - 20))
        screen.blit(level_surf, level_rect)
        pygame.display.flip()
        clock.tick(60)
