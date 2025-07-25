"""
Экран главного меню для Alien Invasion
"""

import pygame

import os
from button import Button
from entities.stars import Star
from settings import Settings


def main_menu():
    # --- Музыкальная кнопка ---
    music_btn_size = 48
    # Загружаем изображения только после установки video mode
    music_on_img = None
    music_off_img = None
    music_btn_rect = None
    music_playing = [True]
    sound_enabled = [True]
    """Главное меню игры. Позволяет выбрать уровень, выйти или начать игру."""
    # Музыка уже запущена глобально, ничего не делаем

    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    clock = pygame.time.Clock()

    class DummyGame:
        def __init__(self, screen):
            self.screen = screen
            self.settings = settings

    dummy_game = DummyGame(screen)

    stars = pygame.sprite.Group()
    for _ in range(200):
        stars.add(Star(dummy_game))

    base_folder = os.path.dirname(os.path.dirname(__file__))
    retro_font_path = os.path.join(base_folder, "fonts&music", "retro_font.otf")
    title_font = pygame.font.Font(retro_font_path, 200)

    button_width = 500
    button_height = 120
    button_spacing = 40
    bottom_margin = 150

    exit_button_y = settings.screen_height - bottom_margin - button_height // 2
    levels_button_y = exit_button_y - button_height - button_spacing
    play_button_y = levels_button_y - button_height - button_spacing

    play_button = Button(
        screen,
        text="Start a Game",
        center=(settings.screen_width // 2, play_button_y),
        width=button_width,
        height=button_height,
        font_path=os.path.join("fonts&music", "retro_font.otf"),
        font_size=50,
        bg_color=(32, 32, 32),
        hover_color=(64, 64, 64),
    )

    levels_button = Button(
        screen,
        text="Levels",
        center=(settings.screen_width // 2, levels_button_y),
        width=button_width,
        height=button_height,
        font_path=os.path.join("fonts&music", "retro_font.otf"),
        font_size=50,
        bg_color=(32, 32, 32),
        hover_color=(64, 64, 64),
    )

    exit_button = Button(
        screen,
        text="Exit",
        center=(settings.screen_width // 2, exit_button_y),
        width=button_width,
        height=button_height,
        font_path=os.path.join("fonts&music", "retro_font.otf"),
        font_size=50,
        bg_color=(32, 32, 32),
        hover_color=(64, 64, 64),
    )

    selected_level = [1]  # Используем список для передачи по ссылке
    show_levels = [False]

    def draw_levels_menu():
        font = pygame.font.Font(retro_font_path, 80)
        level1_btn = Button(
            screen,
            text="Level 1",
            center=(
                settings.screen_width // 2,
                settings.screen_height // 2 - 180,
            ),
            width=400,
            height=100,
            font_path=retro_font_path,
            font_size=50,
        )
        level2_btn = Button(
            screen,
            text="Level 2",
            center=(
                settings.screen_width // 2,
                settings.screen_height // 2 - 60,
            ),
            width=400,
            height=100,
            font_path=retro_font_path,
            font_size=50,
        )
        level3_btn = Button(
            screen,
            text="Level 3",
            center=(
                settings.screen_width // 2,
                settings.screen_height // 2 + 60,
            ),
            width=400,
            height=100,
            font_path=retro_font_path,
            font_size=50,
        )
        level4_btn = Button(
            screen,
            text="Level 4",
            center=(
                settings.screen_width // 2,
                settings.screen_height // 2 + 180,
            ),
            width=400,
            height=100,
            font_path=retro_font_path,
            font_size=50,
        )
        level5_btn = Button(
            screen,
            text="Level 5",
            center=(
                settings.screen_width // 2,
                settings.screen_height // 2 + 300,
            ),
            width=400,
            height=100,
            font_path=retro_font_path,
            font_size=50,
        )
        endless_btn = Button(
            screen,
            text="Endless",
            center=(
                settings.screen_width // 2,
                settings.screen_height // 2 + 420,
            ),
            width=400,
            height=100,
            font_path=retro_font_path,
            font_size=50,
            bg_color=(20, 40, 20),
            hover_color=(40, 80, 40),
        )
        while show_levels[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show_levels[0] = False
                    return "exit"
                if level1_btn.is_clicked(event):
                    selected_level[0] = 1
                    settings.level = 1
                    show_levels[0] = False
                if level2_btn.is_clicked(event):
                    selected_level[0] = 2
                    settings.level = 2
                    show_levels[0] = False
                if level3_btn.is_clicked(event):
                    selected_level[0] = 3
                    settings.level = 3
                    show_levels[0] = False
                if level4_btn.is_clicked(event):
                    selected_level[0] = 4
                    settings.level = 4
                    show_levels[0] = False
                if level5_btn.is_clicked(event):
                    selected_level[0] = 5
                    settings.level = 5
                    show_levels[0] = False
                if endless_btn.is_clicked(event):
                    selected_level[0] = 9999
                    settings.level = 9999
                    show_levels[0] = False
            stars.update()
            screen.fill(settings.bg_color)
            stars.draw(screen)
            title = font.render("Select Level", True, (255, 255, 255))
            screen.blit(
                title,
                title.get_rect(
                    center=(
                        settings.screen_width // 2,
                        settings.screen_height // 2 - 300,
                    )
                ),
            )
            level1_btn.draw()
            level2_btn.draw()
            level3_btn.draw()
            level4_btn.draw()
            level5_btn.draw()
            endless_btn.draw()
            pygame.display.flip()
            clock.tick(60)

    # print("main_menu start")
    pygame.display.update()
    # Загружаем изображения после установки video mode
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

    # --- Синхронизация состояния кнопки с глобальным SOUND_ENABLED ---
    import builtins

    if hasattr(builtins, "SOUND_ENABLED"):
        sound_enabled[0] = bool(builtins.SOUND_ENABLED)
        music_playing[0] = bool(builtins.SOUND_ENABLED)
    else:
        sound_enabled[0] = True
        music_playing[0] = True

    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # print("main_menu exit")
                return "exit"
            if play_button.is_clicked(event):
                # print("main_menu play")
                return selected_level[0]
            if exit_button.is_clicked(event):
                # print("main_menu exit btn")
                return "exit"
            if levels_button.is_clicked(event):
                # print("main_menu levels")
                show_levels[0] = True
                draw_levels_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
        title_text = title_font.render("ALIEN INVASION", True, (255, 255, 255))
        screen.blit(
            title_text,
            title_text.get_rect(
                center=(
                    settings.screen_width // 2,
                    settings.screen_height // 4,
                )
            ),
        )
        play_button.draw()
        levels_button.draw()
        exit_button.draw()
        # Кнопка музыки
        if music_playing[0]:
            screen.blit(music_on_img, (music_btn_rect.x, music_btn_rect.y))
        else:
            screen.blit(music_off_img, (music_btn_rect.x, music_btn_rect.y))

        # Глобально сохраняем состояние звука для игрового процесса
        import builtins

        builtins.SOUND_ENABLED = sound_enabled[0]
        # Отображение уровня в главном меню (белый цвет)
        retro_font_path = os.path.join(base_folder, "fonts&music", "retro_font.otf")
        font = pygame.font.Font(retro_font_path, 48)
        level_surf = font.render(f"Level: {selected_level[0]}", True, (255, 255, 255))
        level_rect = level_surf.get_rect(
            bottomright=(
                settings.screen_width - 20,
                settings.screen_height - 20,
            )
        )
        screen.blit(level_surf, level_rect)
        pygame.display.flip()
        clock.tick(60)
