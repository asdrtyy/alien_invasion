# Alien Invasion Project

## Структура проекта

- `alien_invasion/` — основной пакет игры
    - `alien_invasion.py` — точка входа, основной игровой цикл
    - `entities/` — игровые объекты (Alien, Ship, Bullet, Explosion, Star)
    - `menu.py` — главное меню, меню паузы, game over, level complete
    - `settings.py` — настройки игры
    - `settings_menu.py` — меню настроек
    - `game_state.py` — управление состоянием игры (жизни, очки, уровень, high score)
    - `level_manager.py` — параметры и прогрессия уровней
    - `button.py` — универсальные кнопки интерфейса
    - `fonts/`, `images/` — ресурсы (шрифты, изображения)
    - `screens/` — (зарезервировано для будущих экранов)
    - `tests/` — автоматические тесты логики (GameState, LevelManager и др.)

## Основные классы и модули
- `GameState` — управление жизнями, очками, уровнем, high score
- `LevelManager` — параметры и прогрессия уровней, поддержка бесконечного режима
- `Alien`, `Ship`, `Bullet`, `Explosion`, `Star` — игровые объекты (entities/)
- `main_menu`, `pause_menu`, `game_over_screen`, `level_complete_screen` — экраны (menu.py)
- `Button` — универсальный класс кнопки (button.py)

## Архитектурные принципы
- Вся логика игровых объектов вынесена в entities/
- Состояния игры и уровней централизованы (GameState, LevelManager)
- Все экраны реализованы как отдельные функции (menu.py)
- Тесты не зависят от UI и ресурсов, тестируют только бизнес-логику
- Код приведён к PEP8, снабжён docstring и комментариями

## Как запустить
1. Установить зависимости: `pip install pygame`
2. Запустить `python alien_invasion.py` из папки alien_invasion/


Документация и структура поддерживаются автоматически при изменениях.
