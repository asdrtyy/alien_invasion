"""Модуль состояния игры для Alien Invasion."""

import os


class GameState:
    # Класс для управления состоянием игры: жизни, уровень, очки, high score

    def __init__(self, level=1, lives=3, score=0):
        self.level = level
        self.lives = lives
        self.score = score
        self.running = True
        self.paused = False
        self.game_over = False
        self.high_score = self.load_high_score()

    def lose_life(self):
        """Уменьшает количество жизней на 1. Если жизни закончились, устанавливает состояние игры как 'конец игры'."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def add_score(self, points):
        """Добавляет очки к текущему счету."""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def next_level(self):
        """Переходит на следующий уровень, увеличивая уровень на 1."""
        self.level += 1

    def reset(self, level=1, lives=3, score=0):
        """Сбрасывает состояние игры, устанавливая указанные уровень, жизни и очки."""
        self.level = level
        self.lives = lives
        self.score = score
        self.running = True
        self.paused = False
        self.game_over = False

    def load_high_score(self):
        """Загружает рекордное количество очков из файла highscore.txt."""
        try:
            with open(
                os.path.join(os.path.dirname(__file__), "highscore.txt"), "r"
            ) as f:
                return int(f.read())
        except Exception:
            return 0

    def save_high_score(self):
        """Сохраняет рекордное количество очков в файл highscore.txt."""
        try:
            with open(
                os.path.join(os.path.dirname(__file__), "highscore.txt"), "w"
            ) as f:
                f.write(str(self.high_score))
        except Exception:
            pass
