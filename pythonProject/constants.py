from pygame.locals import *

# Конфигурация блока формы
# Ширина
BWIDTH     = 20
# Высота
BHEIGHT    = 20
# Ширина линии вокруг блока
MESH_WIDTH = 1

# Конфигурация доски игрока
# Высота линии доски
BOARD_HEIGHT     = 7
# Поле верхней строки (для счета)
BOARD_UP_MARGIN  = 40
# Поля вокруг всех строк
BOARD_MARGIN     = 2


# Объявления цветов в RGB
WHITE    = (255,255,255)
RED      = (255,0,0)
GREEN    = (0,255,0)
BLUE     = (0,0,255)
ORANGE   = (255,69,0)
GOLD     = (255,125,0)
PURPLE   = (128,0,128)
CYAN     = (0,255,255)
BLACK    = (0,0,0)

# Временные ограничения
# Время генерации TIME_MOVE_EVENT (мс)
MOVE_TICK          = 1000
# Выделенный номер для события move dowon
TIMER_MOVE_EVENT   = USEREVENT+1
# Коэффициент ускорения игры (целые значения)
GAME_SPEEDUP_RATIO = 1.5
# Score LEVEL - первый порог оценки
SCORE_LEVEL        = 2000
# Соотношение уровней баллов
SCORE_LEVEL_RATIO  = 2

# Конфигурация счета
# Количество баллов за один строительный блок
POINT_VALUE       = 100
#Поле строки score
POINT_MARGIN      = 10

# Размер шрифта для всех строк (счет, пауза, окончание игры)
FONT_SIZE           = 25
