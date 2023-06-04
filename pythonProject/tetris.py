# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import math
import random
import pygame
import block
import constants

class Tetris(object):

    def __init__(self, bx, by):
        # Вычислить разрешение игрового поля на основе необходимого количества блоков.
        self.resx = bx * constants.BWIDTH + 2 * constants.BOARD_HEIGHT + constants.BOARD_MARGIN
        self.resy = by * constants.BHEIGHT + 2 * constants.BOARD_HEIGHT + constants.BOARD_MARGIN
        # Подготовка объектов pygame board
        self.board_up = pygame.Rect(0, constants.BOARD_UP_MARGIN, self.resx, constants.BOARD_HEIGHT)
        self.board_down = pygame.Rect(0, self.resy - constants.BOARD_HEIGHT, self.resx, constants.BOARD_HEIGHT)
        self.board_left = pygame.Rect(0, constants.BOARD_UP_MARGIN, constants.BOARD_HEIGHT, self.resy)
        self.board_right = pygame.Rect(self.resx - constants.BOARD_HEIGHT, constants.BOARD_UP_MARGIN,
                                       constants.BOARD_HEIGHT, self.resy)
        # Список используемых блоков
        self.blk_list = []
        # Вычисление начальных индексов для блоков
        self.start_x = math.ceil(self.resx / 2.0)
        self.start_y = constants.BOARD_UP_MARGIN + constants.BOARD_HEIGHT + constants.BOARD_MARGIN
        # Данные блока (формы и цвета). Форма кодируется в списке точек [X,Y]. Каждая точка
        # представляет относительное положение. Значение true/false используется для конфигурации вращения, где
        # False означает отсутствие поворота, а True разрешает поворот.
        self.block_data = (
            ([[0, 0], [1, 0], [2, 0], [3, 0]], constants.RED, True),  # I block
            ([[0, 0], [1, 0], [0, 1], [-1, 1]], constants.GREEN, True),  # S block
            ([[0, 0], [1, 0], [2, 0], [2, 1]], constants.BLUE, True),  # J block
            ([[0, 0], [0, 1], [1, 0], [1, 1]], constants.ORANGE, False),  # O block
            ([[-1, 0], [0, 0], [0, 1], [1, 1]], constants.GOLD, True),  # Z block
            ([[0, 0], [1, 0], [2, 0], [1, 1]], constants.PURPLE, True),  # T block
            ([[0, 0], [1, 0], [2, 0], [0, 1]], constants.CYAN, True),  # J block
        )
        # Когда количество блоков четное, мы можем использовать его напрямую, но
        # мы должны уменьшить количество блоков в строке на единицу, если число нечетное (из-за используемого поля).
        self.blocks_in_line = bx if bx % 2 == 0 else bx - 1
        self.blocks_in_pile = by
        # Настройка очков
        self.score = 0
        # Текущая скорость
        self.speed = 1
        # Порог уровня оценки
        self.score_level = constants.SCORE_LEVEL

    def apply_action(self):
        for ev in pygame.event.get():
            # Проверяем, не сработала ли кнопка закрытия.
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.unicode == 'q'):
                self.done = True
            # Обнаружение ключевых событий для управления игрой.
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_DOWN:
                    self.active_block.move(0, constants.BHEIGHT)
                if ev.key == pygame.K_LEFT:
                    self.active_block.move(-constants.BWIDTH, 0)
                if ev.key == pygame.K_RIGHT:
                    self.active_block.move(constants.BWIDTH, 0)
                if ev.key == pygame.K_SPACE:
                    self.active_block.rotate()
                if ev.key == pygame.K_p:
                    self.pause()

            # Определение, было ли событие движения запущено таймером.
            if ev.type == constants.TIMER_MOVE_EVENT:
                self.active_block.move(0, constants.BHEIGHT)

    def pause(self):
        # Строка в центре экрана.
        self.print_center(["ПАУЗА", "Нажмите \"p\", чтобы продолжить"])
        pygame.display.flip()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                    return

    def set_move_timer(self):
        # Установка времени для запуска события перемещения. Минимальное допустимое значение – 1.
        speed = math.floor(constants.MOVE_TICK / self.speed)
        speed = max(1, speed)
        pygame.time.set_timer(constants.TIMER_MOVE_EVENT, speed)

    def run(self):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont(pygame.font.get_default_font(), constants.FONT_SIZE)
        self.screen = pygame.display.set_mode((self.resx, self.resy))
        pygame.display.set_caption("Tetris")
        self.set_move_timer()
        self.done = False
        self.game_over = False
        self.new_block = True
        self.print_status_line()
        while not (self.done) and not (self.game_over):
            # Получить блок и запустить игровую логику
            self.get_block()
            self.game_logic()
            self.draw_game()
        # Показать game_over и дождаться нажатия клавиши
        if self.game_over:
            self.print_game_over()
        # Отключить pygame
        pygame.font.quit()
        pygame.display.quit()

    def print_status_line(self):
        string = ["SCORE: {0}   SPEED: {1}x".format(self.score, self.speed)]
        self.print_text(string, constants.POINT_MARGIN, constants.POINT_MARGIN)

    def print_game_over(self):
        self.print_center(["Вы проиграли", "Нажмите \"q\" для выхода"])
        pygame.display.flip()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.unicode == 'q'):
                    return

    def print_text(self, str_lst, x, y):
        prev_y = 0
        for string in str_lst:
            size_x, size_y = self.myfont.size(string)
            txt_surf = self.myfont.render(string, False, (255, 255, 255))
            self.screen.blit(txt_surf, (x, y + prev_y))
            prev_y += size_y

    def print_center(self, str_list):
        max_xsize = max([tmp[0] for tmp in map(self.myfont.size, str_list)])
        self.print_text(str_list, self.resx / 2 - max_xsize / 2, self.resy / 2)

    def block_colides(self):
        for blk in self.blk_list:
            # Проверяем, не совпадает ли блок
            if blk == self.active_block:
                continue
            if (blk.check_collision(self.active_block.shape)):
                return True
        return False

    def game_logic(self):
        # Запомним текущую конфигурацию и применим действие
        self.active_block.backup()
        self.apply_action()
        # Логика границы, проверяем, не сталкиваемся ли мы с нижней границей или любой другой.
        # Эта проверка также включает обнаружение с другими блоками тетриса.
        down_board = self.active_block.check_collision([self.board_down])
        any_border = self.active_block.check_collision([self.board_left, self.board_up, self.board_right])
        block_any = self.block_colides()
        # Восстановить конфигурацию, если было обнаружено какое-либо столкновение
        if down_board or any_border or block_any:
            self.active_block.restore()
        # Пока все хорошо, пробуем предыдущее состояние и пытаемся двигаться вниз.
        # После этого обнаруживаем вставку нового блока. Новый блок вставляется, если мы достигли границы
        # или мы не можем двигаться вниз.
        self.active_block.backup()
        self.active_block.move(0, constants.BHEIGHT)
        can_move_down = not self.block_colides()
        self.active_block.restore()
        # Мы заканчиваем игру, не можем двигаться
        if not can_move_down and (self.start_x == self.active_block.x and self.start_y == self.active_block.y):
            self.game_over = True
        # Новый блок вставляется, если мы достигли нижней доски или не можем двигаться вниз.
        if down_board or not can_move_down:
            # Запросить новый блок
            self.new_block = True
            # Обнаружить заполненную строку и удалить строку с экрана.
            self.detect_line()

    def detect_line(self):
        for shape_block in self.active_block.shape:
            tmp_y = shape_block.y
            tmp_cnt = self.get_blocks_in_line(tmp_y)
            # Определяем, содержит ли строка заданное количество блоков
            if tmp_cnt != self.blocks_in_line:
                continue
            self.remove_line(tmp_y)
            # Обновить счет
            self.score += self.blocks_in_line * constants.POINT_VALUE
            # Проверяем, нужно ли нам ускорить игру
            if self.score > self.score_level:
                self.score_level *= constants.SCORE_LEVEL_RATIO
                self.speed *= constants.GAME_SPEEDUP_RATIO
                # Change the game speed
                self.set_move_timer()

    def remove_line(self, y):
        # Перебираем все блоки в списке и удаляем блоки с координатой Y.
        for block in self.blk_list:
            block.remove_blocks(y)
        # Настроить новый список блоков (ненужные блоки удаляются)
        self.blk_list = [blk for blk in self.blk_list if blk.has_blocks()]

    def get_blocks_in_line(self, y):
        tmp_cnt = 0
        for block in self.blk_list:
            for shape_block in block.shape:
                tmp_cnt += (1 if y == shape_block.y else 0)
        return tmp_cnt

    def draw_board(self):
        pygame.draw.rect(self.screen, constants.WHITE, self.board_up)
        pygame.draw.rect(self.screen, constants.WHITE, self.board_down)
        pygame.draw.rect(self.screen, constants.WHITE, self.board_left)
        pygame.draw.rect(self.screen, constants.WHITE, self.board_right)
        self.print_status_line()

    def get_block(self):
        if self.new_block:
            # Получить блок и добавить его в список блоков
            tmp = random.randint(0, len(self.block_data) - 1)
            data = self.block_data[tmp]
            self.active_block = block.Block(data[0], self.start_x, self.start_y, self.screen, data[1], data[2])
            self.blk_list.append(self.active_block)
            self.new_block = False

    def draw_game(self):
        # Очистка экрана, рисование доски всех блоков тетрис
        self.screen.fill(constants.BLACK)
        self.draw_board()
        for blk in self.blk_list:
            blk.draw()
        pygame.display.flip()


if __name__ == "__main__":
    Tetris(16, 30).run()
