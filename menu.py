"""Модуль меню для Alien Invasion."""

import pygame
import sys
import os
from alien_invasion.settings import Settings
from entities.stars import Star


def dummy_game_setup():
    """Настройка для создания объекта игры без запуска."""
    
    settings = Settings()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    return screen, settings


def create_stars_group(settings, count=200):
    """Создание группы звезд для фона."""

    class DummyGame:
        def __init__(self, screen, settings):
            self.screen = screen
            self.settings = settings

    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode(
            (settings.screen_width, settings.screen_height)
        )
    dummy_game = DummyGame(screen, settings)
    stars = pygame.sprite.Group()
    for _ in range(count):
        stars.add(Star(dummy_game))
    return stars


def draw_title(screen, text, font_path, size, position):
    """Отображение заголовка или текста на экране."""
    font = pygame.font.Font(font_path, size)
    title_surf = font.render(text, True, (255, 255, 255))
    screen.blit(title_surf, title_surf.get_rect(center=position))


def wait_for_keypress():
    """Ожидание нажатия клавиши."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False


def show_message(screen, text, font_path, size, position, duration=2):
    """Показать сообщение на экране на заданное время."""
    font = pygame.font.Font(font_path, size)
    message_surf = font.render(text, True, (255, 255, 255))
    screen.blit(message_surf, message_surf.get_rect(center=position))
    pygame.display.flip()
    pygame.time.delay(duration * 1000)


def run_menu():
    screen, settings = dummy_game_setup()
    stars = create_stars_group(settings)
    base_folder = os.path.dirname(__file__)
    retro_font_path = os.path.join(
        base_folder, "fonts&music", "retro_font.otf"
    )

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        stars.update()
        screen.fill(settings.bg_color)
        stars.draw(screen)
        draw_title(
            screen,
            "ALIEN INVASION",
            retro_font_path,
            200,
            (settings.screen_width // 2, settings.screen_height // 4),
        )
        pygame.display.flip()
        clock.tick(60)
