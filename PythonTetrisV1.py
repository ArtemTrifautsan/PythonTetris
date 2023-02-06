import pygame
import random
import time
import copy

pygame.init()

WIDTH_SCREEN = 520
HEIGHT_SCREEN = 680
FPS = 60

# Game screen
SCREEN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
AQUA = (0, 255, 255)
YELLOW = (225, 225, 0)
PINK = (255, 0, 255)
ORANGE = (255, 125, 0)
DARK_GREEN = (0, 125, 0)

# Blocks` parameters
block_interval = 2
block_width = 40

# The list of the impacted blocks at the SCREEN`s bottom
impacted_blocks = {}


class PinkFig:
    def __init__(self, x, y):
        self.color = PINK
        self.x = x
        self.y = y
        self.blocks = [[self.x-1, self.y], [self.x, self.y], [self.x+1, self.y], [self.x+2, self.y]]
        self.state = 1

    def rotate(self):
        """
        Чтобы повернуть фигуру, функция создаёт её копию, поворачивает и смотрит на пересечение блоков скопированной
        фигуры и блоков impacted_blocks. Если пересечение произошло, фигура не поворачивается
        """
        possible_rotate = True  # Возможность повернуть фигуру
        var_coordinate = 1  # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor = 1    # Коэфициент поворота копии фигуры (нужен для расчётов)
        copy_figure = copy.deepcopy(self.blocks)    # Скопированная фигура

        # Поворот скопированной фигуры для состояния 1
        if self.state == 1:
            var_coor = 1
            copy_figure[0][0] += var_coor
            copy_figure[0][1] -= var_coor
            # Third block
            copy_figure[2][0] -= var_coor
            copy_figure[2][1] += var_coor
            # Fourth block
            copy_figure[3][0] -= var_coor * 2
            copy_figure[3][1] += var_coor * 2

            # Проверка на пересечение блоков фигуры и блоков impacted_blocks
            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        # Поворот скопированной фигуры для состояния 2
        elif self.state == 2:
            var_coor = -1
            copy_figure[0][0] += var_coor
            copy_figure[0][1] -= var_coor
            # Third block
            copy_figure[2][0] -= var_coor
            copy_figure[2][1] += var_coor
            # Fourth block
            copy_figure[3][0] -= var_coor * 2
            copy_figure[3][1] += var_coor * 2

            # Проверка на пересечение блоков фигуры и блоков impacted_blocks
            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        # Процесс поворота фигуры
        if possible_rotate:
            if self.state == 1:
                self.state = 2
                var_coordinate = 1
            else:
                self.state = 1
                var_coordinate = -1
            # First block
            self.blocks[0][0] += var_coordinate
            self.blocks[0][1] -= var_coordinate
            # Third block
            self.blocks[2][0] -= var_coordinate
            self.blocks[2][1] += var_coordinate
            # Fourth block
            self.blocks[3][0] -= var_coordinate * 2
            self.blocks[3][1] += var_coordinate * 2


class GreenFig:
    def __init__(self, x, y):
        self.color = GREEN
        self.x = x
        self.y = y
        self.blocks = [[self.x, self.y], [self.x + 1, self.y], [self.x, self.y + 1], [self.x + 1, self.y + 1]]
        self.state = 1

    def rotate(self):
        pass


class RedFig:
    def __init__(self, x, y):
        self.color = RED
        self.x = x
        self.y = y
        self.blocks = [[self.x - 1, self.y], [self.x, self.y], [self.x + 1, self.y], [self.x + 1, self.y + 1]]
        self.state = 1

    def rotate(self):
        """
        Чтобы повернуть фигуру, функция создаёт её копию, поворачивает и смотрит на пересечение блоков скопированной
        фигуры и блоков impacted_blocks. Если пересечение произошло, фигура не поворачивается
        """
        possible_rotate = True      # Возможность повернуть фигуру
        var_coordinate1 = 1      # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor1 = 1    # Коэфициент поворота копии фигуры (нужен для расчётов)
        var_coordinate2 = 1  # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor2 = 1  # Коэфициент поворота копии фигуры (нужен для расчётов)
        copy_figure = copy.deepcopy(self.blocks)    # Скопированная фигура

        if self.state == 1 or self.state == 3:
            if self.state == 1:
                var_coor1 = 1
            elif self.state == 3:
                var_coor1 = -1

            # First block
            copy_figure[0][0] += var_coor1
            copy_figure[0][1] -= var_coor1
            # Third block
            copy_figure[2][0] -= var_coor1
            copy_figure[2][1] += var_coor1
            # Fourth block
            copy_figure[3][0] -= var_coor1 * 2

            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        elif self.state == 2 or self.state == 4:
            if self.state == 2:
                var_coor2 = 1
            elif self.state == 4:
                var_coor2 = -1

            # First block
            copy_figure[0][0] += var_coor2
            copy_figure[0][1] += var_coor2
            # Third block
            copy_figure[2][0] -= var_coor2
            copy_figure[2][1] -= var_coor2
            # Fourth block
            copy_figure[3][1] -= var_coor2 * 2

            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        if possible_rotate:
            if self.state == 1 or self.state == 3:
                if self.state == 1:
                    self.state = 2
                    var_coordinate1 = 1
                elif self.state == 3:
                    self.state = 4
                    var_coordinate1 = -1

                # First block
                self.blocks[0][0] += var_coordinate1
                self.blocks[0][1] -= var_coordinate1
                # Third block
                self.blocks[2][0] -= var_coordinate1
                self.blocks[2][1] += var_coordinate1
                # Fourth block
                self.blocks[3][0] -= var_coordinate1 * 2

            elif self.state == 2 or self.state == 4:
                if self.state == 2:
                    self.state = 3
                    var_coordinate2 = 1
                elif self.state == 4:
                    self.state = 1
                    var_coordinate2 = -1

                self.blocks[0][0] += var_coordinate2
                self.blocks[0][1] += var_coordinate2
                # Third block
                self.blocks[2][0] -= var_coordinate2
                self.blocks[2][1] -= var_coordinate2
                # Fourth block
                self.blocks[3][1] -= var_coordinate2 * 2


class BlueFig:
    def __init__(self, x, y):
        self.color = BLUE
        self.x = x
        self.y = y
        self.blocks = [[self.x - 1, self.y], [self.x, self.y], [self.x + 1, self.y], [self.x - 1, self.y + 1]]
        self.state = 1

    def rotate(self):
        """
        Чтобы повернуть фигуру, функция создаёт её копию, поворачивает и смотрит на пересечение блоков скопированной
        фигуры и блоков impacted_blocks. Если пересечение произошло, фигура не поворачивается
        """
        possible_rotate = True      # Возможность повернуть фигуру
        var_coordinate1 = 1      # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor1 = 1    # Коэфициент поворота копии фигуры (нужен для расчётов)
        var_coordinate2 = 1  # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor2 = 1  # Коэфициент поворота копии фигуры (нужен для расчётов)
        copy_figure = copy.deepcopy(self.blocks)    # Скопированная фигура

        if self.state == 1 or self.state == 3:
            if self.state == 1:
                var_coor1 = 1
            elif self.state == 3:
                var_coor1 = -1

            # First block
            copy_figure[0][0] += var_coor1
            copy_figure[0][1] -= var_coor1
            # Third block
            copy_figure[2][0] -= var_coor1
            copy_figure[2][1] += var_coor1
            # Fourth block
            copy_figure[3][1] -= var_coor1 * 2

            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        elif self.state == 2 or self.state == 4:
            if self.state == 2:
                var_coor2 = 1
            elif self.state == 4:
                var_coor2 = -1

            # First block
            copy_figure[0][0] += var_coor2
            copy_figure[0][1] += var_coor2
            # Third block
            copy_figure[2][0] -= var_coor2
            copy_figure[2][1] -= var_coor2
            # Fourth block
            copy_figure[3][0] += var_coor2 * 2

            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        if possible_rotate:
            if self.state == 1 or self.state == 3:
                if self.state == 1:
                    self.state = 2
                    var_coordinate1 = 1
                elif self.state == 3:
                    self.state = 4
                    var_coordinate1 = -1

                # First block
                self.blocks[0][0] += var_coordinate1
                self.blocks[0][1] -= var_coordinate1
                # Third block
                self.blocks[2][0] -= var_coordinate1
                self.blocks[2][1] += var_coordinate1
                # Fourth block
                self.blocks[3][1] -= var_coordinate1 * 2

            elif self.state == 2 or self.state == 4:
                if self.state == 2:
                    self.state = 3
                    var_coordinate2 = 1
                elif self.state == 4:
                    self.state = 1
                    var_coordinate2 = -1

                self.blocks[0][0] += var_coordinate2
                self.blocks[0][1] += var_coordinate2
                # Third block
                self.blocks[2][0] -= var_coordinate2
                self.blocks[2][1] -= var_coordinate2
                # Fourth block
                self.blocks[3][0] += var_coordinate2 * 2


class AquaFig:
    def __init__(self, x, y):
        self.color = AQUA
        self.x = x
        self.y = y
        self.blocks = [[self.x - 1, self.y], [self.x, self.y], [self.x + 1, self.y], [self.x, self.y + 1]]
        self.state = 1

    def rotate(self):
        """
        Чтобы повернуть фигуру, функция создаёт её копию, поворачивает и смотрит на пересечение блоков скопированной
        фигуры и блоков impacted_blocks. Если пересечение произошло, фигура не поворачивается
        """
        possible_rotate = True      # Возможность повернуть фигуру
        var_coordinate1 = 1      # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor1 = 1    # Коэфициент поворота копии фигуры (нужен для расчётов)
        var_coordinate2 = 1  # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor2 = 1  # Коэфициент поворота копии фигуры (нужен для расчётов)
        copy_figure = copy.deepcopy(self.blocks)    # Скопированная фигура

        if self.state == 1 or self.state == 3:
            if self.state == 1:
                var_coor1 = 1
            elif self.state == 3:
                var_coor1 = -1

            # First block
            copy_figure[0][0] += var_coor1
            copy_figure[0][1] -= var_coor1
            # Third block
            copy_figure[2][0] -= var_coor1
            copy_figure[2][1] += var_coor1
            # Fourth block
            copy_figure[3][0] -= var_coor1
            copy_figure[3][1] -= var_coor1

            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        elif self.state == 2 or self.state == 4:
            if self.state == 2:
                var_coor2 = 1
            elif self.state == 4:
                var_coor2 = -1

            # First block
            copy_figure[0][0] += var_coor2
            copy_figure[0][1] += var_coor2
            # Third block
            copy_figure[2][0] -= var_coor2
            copy_figure[2][1] -= var_coor2
            # Fourth block
            copy_figure[3][0] += var_coor2
            copy_figure[3][1] -= var_coor2

            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        if possible_rotate:
            if self.state == 1 or self.state == 3:
                if self.state == 1:
                    self.state = 2
                    var_coordinate1 = 1
                elif self.state == 3:
                    self.state = 4
                    var_coordinate1 = -1

                # First block
                self.blocks[0][0] += var_coordinate1
                self.blocks[0][1] -= var_coordinate1
                # Third block
                self.blocks[2][0] -= var_coordinate1
                self.blocks[2][1] += var_coordinate1
                # Fourth block
                self.blocks[3][0] -= var_coordinate1
                self.blocks[3][1] -= var_coordinate1

            elif self.state == 2 or self.state == 4:
                if self.state == 2:
                    self.state = 3
                    var_coordinate2 = 1
                elif self.state == 4:
                    self.state = 1
                    var_coordinate2 = -1

                self.blocks[0][0] += var_coordinate2
                self.blocks[0][1] += var_coordinate2
                # Third block
                self.blocks[2][0] -= var_coordinate2
                self.blocks[2][1] -= var_coordinate2
                # Fourth block
                self.blocks[3][0] += var_coordinate2
                self.blocks[3][1] -= var_coordinate2


class YellowFig:
    def __init__(self, x, y):
        self.color = YELLOW
        self.x = x
        self.y = y
        self.blocks = [[self.x - 1, self.y + 1], [self.x, self.y], [self.x, self.y + 1], [self.x + 1, self.y]]
        self.state = 1

    def rotate(self):
        """
        Чтобы повернуть фигуру, функция создаёт её копию, поворачивает и смотрит на пересечение блоков скопированной
        фигуры и блоков impacted_blocks. Если пересечение произошло, фигура не поворачивается
        """
        possible_rotate = True  # Возможность повернуть фигуру
        var_coordinate = 1  # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor = 1    # Коэфициент поворота копии фигуры (нужен для расчётов)
        copy_figure = copy.deepcopy(self.blocks)    # Скопированная фигура

        # Поворот скопированной фигуры для состояния 1
        if self.state == 1:
            var_coor = 1
            copy_figure[0][1] -= var_coor * 2
            # Third block
            copy_figure[2][0] -= var_coor
            copy_figure[2][1] -= var_coor
            # Fourth block
            copy_figure[3][0] -= var_coor
            copy_figure[3][1] += var_coor

            # Проверка на пересечение блоков фигуры и блоков impacted_blocks
            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        # Поворот скопированной фигуры для состояния 2
        elif self.state == 2:
            var_coor = -1
            copy_figure[0][1] -= var_coor
            # Third block
            copy_figure[2][0] -= var_coor
            copy_figure[2][1] -= var_coor
            # Fourth block
            copy_figure[3][0] -= var_coor
            copy_figure[3][1] += var_coor

            # Проверка на пересечение блоков фигуры и блоков impacted_blocks
            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        # Процесс поворота фигуры
        if possible_rotate:
            if self.state == 1:
                self.state = 2
                var_coordinate = 1
            else:
                self.state = 1
                var_coordinate = -1
            # First block
            self.blocks[0][1] -= var_coordinate * 2
            # Third block
            self.blocks[2][0] -= var_coordinate
            self.blocks[2][1] -= var_coordinate
            # Fourth block
            self.blocks[3][0] -= var_coordinate
            self.blocks[3][1] += var_coordinate


class OrangeFig:
    def __init__(self, x, y):
        self.color = ORANGE
        self.x = x
        self.y = y
        self.blocks = [[self.x - 1, self.y], [self.x, self.y], [self.x, self.y + 1], [self.x + 1, self.y + 1]]
        self.state = 1

    def rotate(self):
        """
        Чтобы повернуть фигуру, функция создаёт её копию, поворачивает и смотрит на пересечение блоков скопированной
        фигуры и блоков impacted_blocks. Если пересечение произошло, фигура не поворачивается
        """
        possible_rotate = True  # Возможность повернуть фигуру
        var_coordinate = 1  # Коэфициент поворота фигуры (нужен для расчётов)
        var_coor = 1    # Коэфициент поворота копии фигуры (нужен для расчётов)
        copy_figure = copy.deepcopy(self.blocks)    # Скопированная фигура

        # Поворот скопированной фигуры для состояния 1
        if self.state == 1:
            var_coor = 1
            copy_figure[0][1] += var_coor
            # Third block
            copy_figure[2][0] -= var_coor
            copy_figure[2][1] -= var_coor
            # Fourth block
            copy_figure[3][0] -= var_coor
            copy_figure[3][1] -= var_coor * 2

            # Проверка на пересечение блоков фигуры и блоков impacted_blocks
            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        # Поворот скопированной фигуры для состояния 2
        elif self.state == 2:
            var_coor = -1
            copy_figure[0][1] += var_coor
            # Third block
            copy_figure[2][0] -= var_coor
            copy_figure[2][1] -= var_coor
            # Fourth block
            copy_figure[3][0] -= var_coor
            copy_figure[3][1] -= var_coor * 2

            # Проверка на пересечение блоков фигуры и блоков impacted_blocks
            for i in copy_figure:
                for j in impacted_blocks.keys():
                    for k in impacted_blocks[j]:
                        if i[0] == k[0] and i[1] == k[1]:
                            possible_rotate = False
                            break

            # Ограничить поворот фигуры пределами игрового поля
            min_block = copy_figure[0]
            max_block = copy_figure[0]
            for i in copy_figure[1:]:
                if i[0] > max_block[0]:
                    max_block = i
                elif i[0] < min_block[0]:
                    min_block = i
            if min_block[0] < 0 or max_block[0] > WIDTH_SCREEN // block_width - 1:
                possible_rotate = False

        # Процесс поворота фигуры
        if possible_rotate:
            if self.state == 1:
                self.state = 2
                var_coordinate = 1
            else:
                self.state = 1
                var_coordinate = -1
            # First block
            self.blocks[0][0] += var_coordinate
            self.blocks[0][1] -= var_coordinate
            # Third block
            self.blocks[2][0] -= var_coordinate
            self.blocks[2][1] -= var_coordinate
            # Fourth block
            self.blocks[3][0] -= var_coordinate * 2


def fall_figure(figure):
    """
    Функция падения фигуры. Здесь все элементы фигуры синхронно двигаются вниз.
    """
    for i in figure.blocks:
        i[1] += 1


def turn_figure(figure):
    """
    Функция поворота фигуры. Есть 7 типов фигур, каждый из которых поворачивается по-своему. Поворот осужествляется
    вокруг центрального блока.
    """
    print('Поворот произошёл')
    if figure[0] == PINK:
        # block 2
        figure[2][0] += 1
    pass


def move_figure(figure, direction):
    step = 1 if direction == 'RIGHT' else -1
    min_block = figure.blocks[0]
    max_block = figure.blocks[0]

    for i in figure.blocks[1:]:
        if i[0] < min_block[0]:
            min_block = i
        elif i[0] > max_block[0]:
            max_block = i

    obstacle_blocks = []
    if (min_block[0] > 0 and step == -1) or (max_block[0] < WIDTH_SCREEN // block_width - 1 and step == 1):
        for i in figure.blocks:
            for k in impacted_blocks.keys():
                for j in impacted_blocks[k]:
                    if i[1] == j[1]:
                        if step == 1:
                            if i[0] - j[0] == -1:
                                obstacle_blocks.append(j)
                        elif step == -1:
                            if i[0] - j[0] == 1:
                                obstacle_blocks.append(j)

        if not obstacle_blocks:
            for i in figure.blocks:
                i[0] += step


def impact_figure(figure):
    # Находим самый нижний блок фигуры.
    # Так как таких может быть несколько, находим все.
    bottom_blocks = [figure.blocks[0]]  # Самые нижние блоки фигуры
    for i in figure.blocks[1:]:
        if i[1] > bottom_blocks[0][1]:
            bottom_blocks[0] = i
    for i in figure.blocks:
        if i[1] == bottom_blocks[0][1]:
            bottom_blocks.append(i)

    if impacted_blocks:
        obstacle_blocks = []    # Список блоков, расположенных под фигурой
        for i in figure.blocks:     # Ищем препятствующие блоки для каждого блока фигуры
            for j in impacted_blocks.keys():
                for k in impacted_blocks[j]:
                    if i[0] == k[0] and i[1] < k[1]:
                        obstacle_blocks.append(k)

        # Проверяем, столкнулась ли фигура с каким-либо блоком
        if obstacle_blocks:
            for i in figure.blocks:
                for j in obstacle_blocks:
                    if i[0] == j[0]:
                        if j[1] - i[1] == 1:
                            return True
        else:
            # Если на пути нет блоков, проверяем столкновение фигуры с дном
            if bottom_blocks[0][1] >= HEIGHT_SCREEN // block_width - 1:
                return True

    else:
        # Если на игровом поле вообще нет блоков, проверяем столкновение фигуры с дном
        if bottom_blocks[0][1] >= HEIGHT_SCREEN // block_width - 1:
            return True
        else:
            return False


def clear_level():
    high_blocks = []
    for i in impacted_blocks.keys():
        if len(impacted_blocks[i]) == WIDTH_SCREEN // block_width:
            impacted_blocks[i] = []
            for j in impacted_blocks.keys():
                if j < i:
                    for k in impacted_blocks[j]:
                        k[1] += 1


def lose_game():
    loss = False
    for i in impacted_blocks.keys():
        for j in impacted_blocks[i]:
            if j[1] < 1:
                loss = True
    return loss


def draw_figure(figure):
    for i in figure.blocks:
        draw_block((i[0] * block_width, i[1] * block_width), figure.color)


def draw_block(coordinates, color):
    pygame.draw.rect(SCREEN, BLACK,
                     (coordinates[0] + block_interval, coordinates[1] + block_interval,
                      block_width - block_interval*2, block_width - block_interval*2))
    pygame.draw.rect(SCREEN, color,
                     (coordinates[0] + block_interval*3, coordinates[1] + block_interval*3,
                      block_width - block_interval*6, block_width - block_interval*6))


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# Переменная impact отвечает за столкновение фигуры с нижними блоками.
# Если значение False, движение фигуры вниз продолжается. Если True, тогда создаётся новая фигура
impact = False

# Переменная fall отвечает за движение фигуры вниз. На каждом игровом цикле ей добавляется 1.
# Если значение переменной fall делится без остатка на 60, фигура делает шаг вниз.
fall = 0

random_class_figure = random.choice([PinkFig, GreenFig, RedFig, BlueFig, AquaFig, YellowFig, OrangeFig])
figure = random_class_figure(6, 0)
running = True
while running:
    # Обработка событий
    for events in pygame.event.get():

        # Exit
        if events.type == pygame.QUIT:
            running = False

        # Поворот фигуры
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_UP:
                figure.rotate()
            elif events.key == pygame.K_RIGHT:
                move_figure(figure, 'RIGHT')
            elif events.key == pygame.K_LEFT:
                move_figure(figure, 'LEFT')
            elif events.key == pygame.K_DOWN:
                impact = impact_figure(figure)
                if not impact:
                    fall_figure(figure)

    fall += 1
    impact = impact_figure(figure)
    if impact:
        impact = False

        # 1) Добавить в impacted_blocks блоки столкнувшейся фигуры
        for i in figure.blocks:
            key = impacted_blocks.get(i[1])
            if key is None:
                impacted_blocks[i[1]] = []
            impacted_blocks[i[1]].append([i[0], i[1], figure.color])

        # 2) Создать новую фигуру
        random_class_figure = random.choice([PinkFig, GreenFig, RedFig, BlueFig, AquaFig, YellowFig, OrangeFig])
        figure = random_class_figure(6, 0)

    else:
        if fall % 60 == 0:
            fall_figure(figure)

    # Отрисовка
    SCREEN.fill((175, 207, 199))
    for i in impacted_blocks.keys():
        for j in impacted_blocks[i]:
            draw_block((j[0] * block_width, j[1] * block_width), j[2])
    draw_figure(figure)

    # Условие проигрыша
    if lose_game():
        time.sleep(2)
        running = False

    clear_level()  # Проверить, заполнен ли какой-то из уровней

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
