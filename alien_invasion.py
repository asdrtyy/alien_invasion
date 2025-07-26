"""Alien Invasion — основной игровой модуль."""

import sys
import os
import pygame

from entities.alien import Alien
from entities.ship import Ship
from entities.bullet import Bullet
from entities.explosion import Explosion
from entities.stars import Star

from screens.main_menu import main_menu
from screens.pause_menu import pause_menu
from screens.game_over_screen import game_over_screen
from screens.level_complete_screen import level_complete_screen

from settings import Settings
from game_state import GameState
from level_manager import LevelManager


def play_background_music():
    """Глобальный запуск фоновой музыки."""
    music_path = os.path.join(
        os.path.dirname(__file__), "fonts&music", "background.mp3"
    )
    try:
        pygame.mixer.init()
        if os.path.exists(music_path) and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
    except Exception:
        pass


class AlienInvasion:
    """Главный класс игры Alien Invasion."""

    def __init__(self, level=1):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        previous_lives = getattr(self, "ship", None)
        if previous_lives:
            self.ship = Ship(self, lives=previous_lives.lives)
        else:
            self.ship = Ship(self)
        self.ship.center_ship()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.level_manager = LevelManager()
        self.endless_mode = level == 9999
        # Приводим level к int, если это строка (например, после main_menu)
        try:
            level = int(level)
        except Exception:
            level = 1
        self.state = GameState(
            level=1 if self.endless_mode else level,
            lives=getattr(self.settings, "lives", 3),
        )
        self._create_fleet()
        self._create_stars()
        self.paused = False
        self.game_active = True
        self.collision_flash_time = 0
        self._was_animating = False

        # Музыкальная кнопка (для обратной совместимости)
        self.music_on_img = None
        self.music_off_img = None
        self.music_btn_size = 48
        self.music_btn_rect = None
        self.music_playing = True

    def run_game(self):
        """Основной игровой цикл."""
        while self.game_active:
            self._check_events()
            if self.game_active and not self.paused:
                self.ship.update()
            self._update_bullets()
            self._update_aliens()
            # ...existing code...
            self.stars.update()
            self.explosions.update()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_btn_rect.collidepoint(event.pos):
                    self._toggle_music()

    def _toggle_music(self):
        if self.music_playing:
            pygame.mixer.music.pause()
            self.music_playing = False
        else:
            pygame.mixer.music.unpause()
            self.music_playing = True

    def _check_keydown_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            self._pause_menu()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.aliens, self.bullets, False, True)
        if collisions:
            try:
                import builtins

                if getattr(builtins, "SOUND_ENABLED", True):
                    explosion_sound_path = os.path.join(
                        os.path.dirname(__file__),
                        "fonts&music",
                        "explosion.wav",
                    )
                    if os.path.exists(explosion_sound_path):
                        explosion_sound = pygame.mixer.Sound(explosion_sound_path)
                        explosion_sound.set_volume(0.1)
                        explosion_sound.play()
            except Exception:
                pass
            for alien, bullets in collisions.items():
                if hasattr(alien, "health"):
                    alien.health -= len(bullets)
                    if alien.health <= 0:
                        center = alien.rect.center
                        size = (alien.rect.width, alien.rect.height)
                        alien.kill()
                        explosion = Explosion(center, size=size)
                        self.explosions.add(explosion)
                        self.state.add_score(100)
        if not self.aliens and not self.explosions:
            is_last_level = not self.endless_mode and self.state.level >= 5
            result = level_complete_screen(
                self.screen,
                self.stars,
                self.settings,
                self.state.level,
                is_last_level=is_last_level,
            )
            if result == "continue" and not is_last_level:
                self.state.next_level()
                self._create_fleet()
                self.bullets.empty()
            elif result == "menu" or (is_last_level and result == "continue"):
                level = main_menu()
                self.__init__(level=level)
                self.run_game()

    def _update_aliens(self):
        # Скорость пришельцев зависит от уровня
        base_speed = 0.3  # минимальная скорость
        speed = base_speed * (2 ** (self.state.level - 1))
        speed = min(speed, 1.2)  # максимальная скорость 1.2

        # Все пришельцы движутся только вниз
        for alien in self.aliens.sprites():
            if not hasattr(alien, "y"):
                alien.y = float(alien.rect.y)
            alien.y += speed
            alien.rect.y = int(alien.y)
            alien.rect.x = int(alien.rect.x)

        # Проверка столкновения с кораблем
        if not self.ship.is_animating:
            collided_alien = pygame.sprite.spritecollideany(self.ship, self.aliens)
            if collided_alien:
                try:
                    import builtins

                    if getattr(builtins, "SOUND_ENABLED", True):
                        explosion_sound_path = os.path.join(
                            os.path.dirname(__file__),
                            "fonts&music",
                            "explosion.wav",
                        )
                        if os.path.exists(explosion_sound_path):
                            explosion_sound = pygame.mixer.Sound(explosion_sound_path)
                            explosion_sound.set_volume(0.3)
                            explosion_sound.play()
                except Exception:
                    pass
                self.ship.start_death_animation()
                self.collision_flash_time = pygame.time.get_ticks() + 300
                self.bullets.empty()

        #  Уменьшение количества жизней после завершения анимации
        if self._was_animating and not self.ship.is_animating:
            self.ship.lives -= 1
            if self.ship.lives <= 0:
                self._game_over_screen()

        self._was_animating = self.ship.is_animating



    def _create_fleet(self):
        # Количество полос зависит от уровня: 1 — одна, 2 — две, 3 и выше — три
        params = self.level_manager.get_level_params(self.state.level)
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        interval = max(int(alien_width * 0.3), 10)
        number_aliens_x = (self.settings.screen_width - alien_width) // (
            alien_width + interval
        )
        alien_health = params["alien_health"]
        number_lines = min(max(self.state.level, 1), 3)
        self.aliens_arrival_y = 80
        self.aliens_arrived = False
        for line in range(number_lines):
            y_pos = line * (alien_height + 10)
            total_width = (
                number_aliens_x * alien_width + (number_aliens_x - 1) * interval
            )
            start_x = max((self.settings.screen_width - total_width) // 2, 0)
            for alien_number in range(number_aliens_x):
                x_pos = start_x + alien_number * (alien_width + interval)
                self._create_alien_line(x_pos, y_pos, alien_health)
        self.aliens_spawn_time = pygame.time.get_ticks()

    def _create_alien_line(self, x, y, health=1):
        alien = Alien(self)
        alien.rect.x = x
        alien.rect.y = y
        alien.health = health
        self.aliens.add(alien)

    def _create_alien(self, alien_number, row_number, health=1):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        alien.health = health
        self.aliens.add(alien)

    def _create_stars(self):
        for _ in range(200):
            star = Star(self)
            self.stars.add(star)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.explosions.draw(self.screen)
        # Кнопка музыки убрана из игрового процесса
        if (
            self.collision_flash_time
            and pygame.time.get_ticks() < self.collision_flash_time
        ):
            pygame.draw.rect(self.screen, (255, 0, 0), self.screen.get_rect(), 10)
        live_img_path = os.path.join(os.path.dirname(__file__), "images", "live.png")
        live_img = pygame.image.load(live_img_path).convert_alpha()
        live_img = pygame.transform.scale(live_img, (80, 80))
        for i in range(self.ship.lives):
            x = 15 + i * 65
            y = self.settings.screen_height - 70
            self.screen.blit(live_img, (x, y))
        retro_font_path = os.path.join(
            os.path.dirname(__file__), "fonts&music", "retro_font.otf"
        )
        font = pygame.font.Font(retro_font_path, 48)
        level = getattr(self.settings, "level", self.state.level)
        level_surf = font.render(f"Level: {level}", True, (255, 255, 255))
        level_rect = level_surf.get_rect(
            bottomright=(
                self.settings.screen_width - 20,
                self.settings.screen_height - 20,
            )
        )
        self.screen.blit(level_surf, level_rect)
        score_surf = font.render(f"Score: {self.state.score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(topright=(self.settings.screen_width - 20, 20))
        self.screen.blit(score_surf, score_rect)
        high_score_surf = font.render(
            f"High Score: {self.state.high_score}", True, (255, 215, 0)
        )
        high_score_rect = high_score_surf.get_rect(
            topright=(self.settings.screen_width - 20, 70)
        )
        self.screen.blit(high_score_surf, high_score_rect)
        pygame.display.flip()

    def _pause_menu(self):
        result = pause_menu(self.screen, self.stars, self.settings, self.state.level)
        if result == "menu":
            level = main_menu()
            if level == "exit":
                self.game_active = False
                return
            self.__init__(level=level)

    def _game_over_screen(self):
        result = game_over_screen(
            self.screen, self.stars, self.settings, self.state.level
        )
        if result == "restart":
            self.__init__(level=self.state.level)
            self.ship.lives = 3  # <-- ОБЯЗАТЕЛЬНО сбрасываем жизни
            self.run_game()
        elif result == "menu":
            level = main_menu()
            if level == "exit":
                self.game_active = False
                return
            self.__init__(level=level)
            self.ship.lives = 3  # <-- и здесь тоже сброс жизней
            self.run_game()

# Точка входа


if __name__ == "__main__":
    pygame.init()
    play_background_music()
    level = main_menu()
    if level == "exit":
        sys.exit()
    ai = AlienInvasion(level=level)
    ai.run_game()
