import pygame, buttons
from pygame.locals import *

import menu
import tetris

# Initialize pygame
pygame.init()

from pygame.locals import *
import constants
import records

class Menu(object):

    def __init__(self):
        self.main()


    # Create a display
    def display(self):
        self.resx = 16 * constants.BWIDTH + 2 * constants.BOARD_HEIGHT + constants.BOARD_MARGIN
        self.resy = 30 * constants.BHEIGHT + 2 * constants.BOARD_HEIGHT + constants.BOARD_MARGIN
        self.board_up = pygame.Rect(0, constants.BOARD_UP_MARGIN, self.resx, constants.BOARD_HEIGHT)
        self.board_down = pygame.Rect(0, self.resy - constants.BOARD_HEIGHT, self.resx, constants.BOARD_HEIGHT)
        self.board_left = pygame.Rect(0, constants.BOARD_UP_MARGIN, constants.BOARD_HEIGHT, self.resy)
        self.board_right = pygame.Rect(self.resx - constants.BOARD_HEIGHT, constants.BOARD_UP_MARGIN,
                                       constants.BOARD_HEIGHT, self.resy)
        self.screen = pygame.display.set_mode((self.resx, self.resy))
        self.screen.fill(constants.BLACK)
        pygame.draw.rect(self.screen, constants.WHITE, self.board_up)
        pygame.draw.rect(self.screen, constants.WHITE, self.board_down)
        pygame.draw.rect(self.screen, constants.WHITE, self.board_left)
        pygame.draw.rect(self.screen, constants.WHITE, self.board_right)
        pygame.display.set_caption("Меню")

    # Update the display and show the button
    def update_display(self):
        self.screen.fill(constants.BLACK)

        # Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        pygame.display.flip()

    # Run the loop
    def main(self):
        self.button1 = buttons.buttons()
        self.button2 = buttons.buttons()
        self.display()
        self.update_display()
        while True:
            self.button1.create_button(self.screen, constants.WHITE, 70, 100, 200, 20, 0, "Новая игра",
                                       constants.BLACK)
            self.button2.create_button(self.screen, constants.WHITE, 70, 140, 200, 20, 0, "Рекорды", constants.BLACK)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.button1.pressed(pygame.mouse.get_pos()):
                        self.open_game()
                    elif self.button2.pressed(pygame.mouse.get_pos()):
                        self.open_records()

    def open_game(self):
        """ Открыть 2 окно """
        if __name__ == '__main__':
            tetris.Tetris(16,30).run()
    def open_records(self):
        """ Открыть 2 окно """
        if __name__ == '__main__':
            records.Button_Example().run()







if __name__ == '__main__':
    Menu().run()
