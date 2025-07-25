"""Модуль настроек для Alien Invasion."""


class Settings:
    # Класс для хранения настроек игры

    def __init__(self):
        # Параметры экрана
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 53)  # Цвет фона

        # Параметры корабля
        self.ship_speed = 4.5

        # Параметры пули
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 69, 0)  # Цвет пули
        self.bullets_allowed = float("inf")  # Неограниченное количество пуль

        # Параметры пришельцев
        self.alien_speed = 0.3
        self.fleet_drop_speed = (
            0.1  # Скорость движения пришельцев вниз (уменьшена в 10 раз)
        )
        self.fleet_direction = 1  # 1 — вправо, -1 — влево
