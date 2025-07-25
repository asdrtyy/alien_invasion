"""Модуль управления уровнями для Alien Invasion."""

class LevelManager:
    # Класс для управления параметрами уровней
    def __init__(self):
        self.levels = {
            1: {"alien_health": 1, "rows": 2},
            2: {"alien_health": 2, "rows": 3},
            3: {"alien_health": 2, "rows": 3},
            4: {"alien_health": 3, "rows": 3},
            5: {"alien_health": 4, "rows": 3},
        }

    def get_level_params(self, level):
        """Возвращает параметры уровня по номеру (ограничение: максимум 3 ряда)."""
        if level in self.levels:
            return self.levels[level]
        else:
            alien_health = 1 + (level // 2)
            rows = min(3, 2 + (level // 2))
            return {"alien_health": alien_health, "rows": rows}

    def add_level(self, level, params):
        """Добавляет или обновляет параметры уровня."""
        self.levels[level] = params
