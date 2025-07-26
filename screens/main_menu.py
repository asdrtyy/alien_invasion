"""
Экран главного меню для Alien Invasion
"""

import pygame
import os
from button import Button
from entities.stars import Star
from settings import Settings

# Загрузка количества разблокированных уровней
UNLOCK_FILE = "unlocked_levels.txt"


def load_unlocked_levels():
    try:
        with open(UNLOCK_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 1


def save_unlocked_levels(level):
    with open(UNLOCK_FILE, "w") as f:
        f.write(str(level))


def main_menu():
    music_btn_size = 48
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

    selected_level = [1]
    unlocked_levels = load_unlocked_levels()
    show_levels = [False]
    COLOR_UNLOCKED = (20, 40, 20)
    COLOR_UNLOCKED_HOVER = (40, 80, 40)
    COLOR_LOCKED = (50, 20, 20)

    def draw_levels_menu():
        level_buttons = []
        level_names = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
        spacing = 120
        start_y = settings.screen_height // 2 - 180

        for i, name in enumerate(level_names):
            level_index = i + 1
            is_unlocked = level_index <= unlocked_levels

            btn = Button(
                screen,
                text=name,
                center=(settings.screen_width // 2, start_y + i * spacing),
                width=400,
                height=100,
                font_path=retro_font_path,
                font_size=50,
                bg_color=COLOR_UNLOCKED if is_unlocked else COLOR_LOCKED,
                hover_color=COLOR_UNLOCKED_HOVER if is_unlocked else COLOR_LOCKED,
            )
            level_buttons.append((btn, level_index, is_unlocked))

        if unlocked_levels >= 5:
            endless_btn = Button(
                screen,
                text="Endless",
                center=(settings.screen_width // 2, start_y + 5 * spacing),
                width=400,
                height=100,
                font_path=retro_font_path,
                font_size=50,
                bg_color=COLOR_UNLOCKED,
                hover_color=COLOR_UNLOCKED_HOVER,
            )
            level_buttons.append((endless_btn, True))

        selecting = True
        font = pygame.font.Font(retro_font_path, 80)

        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"

                for btn, lvl, is_unlocked in level_buttons:
                    if is_unlocked and btn.is_clicked(event):
                        return lvl  # Возвращаем выбранный уровень

            stars.update()
            screen.fill(settings.bg_color)
            stars.draw(screen)

            title = font.render("Select Level", True, (255, 255, 255))
            screen.blit(
                title,
                title.get_rect(center=(settings.screen_width // 2, start_y - 120)),
            )

            for btn, _, _ in level_buttons:
                btn.draw()

            pygame.display.flip()
            clock.tick(60)

    pygame.display.update()
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

    import builtins

    music_playing = [True]
    sound_enabled = [True]
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
                return "exit"
            if play_button.is_clicked(event):
                return selected_level[0]
            if exit_button.is_clicked(event):
                return "exit"
            if levels_button.is_clicked(event):
                show_levels[0] = True
                lvl = draw_levels_menu()  # Получаем выбранный уровень из меню
                if isinstance(lvl, int):
                    selected_level[0] = lvl
                    settings.level = lvl
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
                center=(settings.screen_width // 2, settings.screen_height // 4)
            ),
        )
        play_button.draw()
        levels_button.draw()
        exit_button.draw()

        if music_playing[0]:
            screen.blit(music_on_img, (music_btn_rect.x, music_btn_rect.y))
        else:
            screen.blit(music_off_img, (music_btn_rect.x, music_btn_rect.y))

        builtins.SOUND_ENABLED = sound_enabled[0]
        font = pygame.font.Font(retro_font_path, 48)
        level_surf = font.render(f"Level: {selected_level[0]}", True, (255, 255, 255))
        level_rect = level_surf.get_rect(
            bottomright=(settings.screen_width - 20, settings.screen_height - 20)
        )
        screen.blit(level_surf, level_rect)
        pygame.display.flip()
        clock.tick(60)
