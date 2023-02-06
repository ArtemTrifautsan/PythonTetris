import pygame
import random
import colors   # Цвета в отдельном модуле
import copy
import time


pygame.init()

# Основные параметры
# 2 игровых области по 420 пикселей, 2 инфообласти по 150 пикселей + 30 пикселей, делящих игровые области
# Ширина и высота экрана выражена в блоках, помещающихся в экран, а не в пиксилях
WIDTH_SCREEN = 39
HEIGHT_SCREEN = 21
SCREEN = pygame.display.set_mode((WIDTH_SCREEN * 35, HEIGHT_SCREEN * 35))
clock = pygame.time.Clock()
FPS = 60


class Area:
    """
    Класс для игровых и инфообластей. Их координаты, а также ширина и высота выражены не в пикселях, а в количестве
    помещающихся в них блоков
    """
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.x * Block.WIDTH, self.y * Block.WIDTH,
                                              self.width * Block.WIDTH, self.height * Block.WIDTH))


class Block:
    WIDTH = 35  # Длина ребра блока
    INTERVAL = 1    # Интервал между блоками

    def __init__(self, x, y, color, width=WIDTH, interval=INTERVAL):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.interval = interval

    def draw(self):
        pygame.draw.rect(SCREEN, colors.BLOCK_SIDE,
                         (self.x * self.width + self.interval, self.y * self.width + self.interval,
                          self.width - self.interval * 2, self.width - self.interval * 2), border_radius=5)
        pygame.draw.rect(SCREEN, self.color,
                         (self.x * self.width + self.interval * 4, self.y * self.width + self.interval * 4,
                          self.width - self.interval * 8, self.width - self.interval * 8), border_radius=5)


class OrangeFigure:
    def __init__(self, x, y):
        self.color = colors.orange
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x + 1, self.y, self.color), Block(self.x + 2, self.y, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Third block
        self.blocks[2].x -= step
        self.blocks[2].y += step
        # Fourth block
        self.blocks[3].x -= step * 2
        self.blocks[3].y += step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Third block
        self.blocks[2].x -= step
        self.blocks[2].y -= step
        # Fourth block
        self.blocks[3].x -= step * 2
        self.blocks[3].y -= step * 2


class BlueFigure:
    def __init__(self, x, y):
        self.color = colors.blue
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x + 1, self.y, self.color), Block(self.x + 1, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Third block
        self.blocks[2].x -= step
        self.blocks[2].y += step
        # Fourth block
        self.blocks[3].x -= step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Third block
        self.blocks[2].x -= step
        self.blocks[2].y -= step
        # Fourth block
        self.blocks[3].y -= step * 2


class GreenFigure:
    def __init__(self, x, y):
        self.color = colors.green
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x + 1, self.y, self.color), Block(self.x - 1, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Third block
        self.blocks[2].x -= step
        self.blocks[2].y += step
        # Fourth block
        self.blocks[3].y -= step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Third block
        self.blocks[2].x -= step
        self.blocks[2].y -= step
        # Fourth block
        self.blocks[3].x += step * 2


class RedFigure:
    def __init__(self, x, y):
        self.color = colors.red
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x - 1, self.y + 1, self.color), Block(self.x, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Fourth block
        self.blocks[3].x -= step
        self.blocks[3].y -= step
        # Third block
        self.blocks[2].y -= step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Fourth block
        self.blocks[3].x += step
        self.blocks[3].y -= step
        # Third block
        self.blocks[2].x += step * 2


class AquaFigure:
    def __init__(self, x, y):
        self.color = colors.aqua
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x + 1, self.y, self.color), Block(self.x, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Fourth block
        self.blocks[2].x -= step
        self.blocks[2].y += step
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y -= step

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Fourth block
        self.blocks[2].x -= step
        self.blocks[2].y -= step
        # Third block
        self.blocks[3].x += step
        self.blocks[3].y -= step


class PinkFigure:
    def __init__(self, x, y):
        self.color = colors.pink
        self.x = x
        self.y = y
        self.blocks = [Block(self.x, self.y, self.color), Block(self.x + 1, self.y, self.color),
                       Block(self.x - 1, self.y + 1, self.color), Block(self.x, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[1].x -= step
        self.blocks[1].y += step
        # Fourth block
        self.blocks[2].y -= step * 2
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y -= step

    def rotate2(self, step):
        # First block
        self.blocks[1].x -= step
        self.blocks[1].y -= step
        # Fourth block
        self.blocks[2].x += step * 2
        # Third block
        self.blocks[3].x += step
        self.blocks[3].y -= step


class YellowFigure:
    def __init__(self, x, y):
        self.color = colors.yellow
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x, self.y + 1, self.color), Block(self.x + 1, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Fourth block
        self.blocks[2].x -= step
        self.blocks[2].y -= step
        # Third block
        self.blocks[3].x -= step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Fourth block
        self.blocks[2].x += step
        self.blocks[2].y -= step
        # Third block
        self.blocks[3].y -= step * 2


class DarkGreenFigure:
    def __init__(self, x, y):
        self.color = colors.dark_green
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x, self.y + 1, self.color), Block(self.x + 1, self.y + 1, self.color),
                       Block(self.x + 1, self.y + 2, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Fourth block
        self.blocks[2].x -= step
        self.blocks[2].y -= step
        # Third block
        self.blocks[3].x -= step * 2
        # Fifth block
        self.blocks[4].x -= step * 3
        self.blocks[4].y -= step

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Fourth block
        self.blocks[2].x += step
        self.blocks[2].y -= step
        # Third block
        self.blocks[3].y -= step * 2
        # Fifth block
        self.blocks[4].x += step
        self.blocks[4].y -= step * 3


class PurpleFigure:
    def __init__(self, x, y):
        self.color = colors.purple
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y + 1, self.color), Block(self.x - 1, self.y, self.color),
                       Block(self.x, self.y, self.color), Block(self.x + 1, self.y, self.color),
                       Block(self.x + 1, self.y - 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].y -= step * 2
        # Fourth block
        self.blocks[1].x += step
        self.blocks[1].y -= step
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y += step
        # Fifth block
        self.blocks[4].y += step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step * 2
        # Fourth block
        self.blocks[1].x += step
        self.blocks[1].y += step
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y -= step
        # Fifth block
        self.blocks[4].x -= step * 2


class LavenderFigure:
    def __init__(self, x, y):
        self.color = colors.lavender
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y - 1, self.color), Block(self.x - 1, self.y, self.color),
                       Block(self.x, self.y, self.color), Block(self.x + 1, self.y, self.color),
                       Block(self.x + 1, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step * 2
        # Fourth block
        self.blocks[1].x += step
        self.blocks[1].y -= step
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y += step
        # Fifth block
        self.blocks[4].x -= step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].y += step * 2
        # Fourth block
        self.blocks[1].x += step
        self.blocks[1].y += step
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y -= step
        # Fifth block
        self.blocks[4].y -= step * 2


class KhakiFigure:
    def __init__(self, x, y):
        self.color = colors.khaki
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 1, self.y, self.color), Block(self.x, self.y, self.color),
                       Block(self.x, self.y - 1, self.color), Block(self.x, self.y + 1, self.color),
                       Block(self.x + 1, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y -= step
        # Fourth block
        self.blocks[2].x += step
        self.blocks[2].y += step
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y -= step
        # Fifth block
        self.blocks[4].x -= step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Fourth block
        self.blocks[2].x -= step
        self.blocks[2].y += step
        # Third block
        self.blocks[3].x += step
        self.blocks[3].y -= step
        # Fifth block
        self.blocks[4].y -= step * 2


class MaroonFigure:
    def __init__(self, x, y):
        self.color = colors.maroon
        self.x = x
        self.y = y
        self.blocks = [Block(self.x, self.y - 1, self.color), Block(self.x, self.y, self.color),
                       Block(self.x + 1, self.y, self.color), Block(self.x, self.y + 1, self.color),
                       Block(self.x - 1, self.y + 1, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        self.blocks[0].y += step
        # Fourth block
        self.blocks[2].x -= step
        self.blocks[2].y += step
        # Third block
        self.blocks[3].x -= step
        self.blocks[3].y -= step
        # Fifth block
        self.blocks[4].y -= step * 2

    def rotate2(self, step):
        # First block
        self.blocks[0].x -= step
        self.blocks[0].y += step
        # Fourth block
        self.blocks[2].x -= step
        self.blocks[2].y -= step
        # Third block
        self.blocks[3].x += step
        self.blocks[3].y -= step
        # Fifth block
        self.blocks[4].x += step * 2


class DarkFigure1:
    def __init__(self, x, y):
        self.color = colors.dark_green
        self.x = x
        self.y = y
        self.blocks = [Block(self.x - 3, self.y + 1, self.color), Block(self.x, self.y, self.color),
                       Block(self.x - 2, self.y + 1, self.color), Block(self.x - 3, self.y + 2, self.color),
                       Block(self.x - 1, self.y + 2, self.color), Block(self.x, self.y + 2, self.color),
                       Block(self.x + 2, self.y - 1, self.color), Block(self.x - 2, self.y + 3, self.color),
                       Block(self.x - 2, self.y + 4, self.color), Block(self.x - 1, self.y + 4, self.color),
                       Block(self.x, self.y + 4, self.color), Block(self.x + 2, self.y + 3, self.color)]
        self.state = 1

    def rotate1(self, step):
        # First block
        self.blocks[0].x += step
        # Fourth block
        self.blocks[2].y += step
        # Third block
        self.blocks[3].y -= step
        # Fifth block
        self.blocks[4].x += step
        # Fifth block
        self.blocks[5].x += step
        # Fifth block
        self.blocks[6].y -= step
        # Fifth block
        self.blocks[7].x += step
        # Fifth block
        self.blocks[8].x -= step
        # Fifth block
        self.blocks[9].x -= step
        # Fifth block
        self.blocks[10].x -= step
        # Fifth block
        self.blocks[11].x -= step

    def rotate2(self, step):
        # First block
        self.blocks[0].y -= step
        # Fourth block
        self.blocks[2].y += step
        # Third block
        self.blocks[3].x -= step
        # Fifth block
        self.blocks[4].x -= step
        # Fifth block
        self.blocks[5].y -= step
        # Fifth block
        self.blocks[6].x += step
        # Fifth block
        self.blocks[7].x += step
        # Fifth block
        self.blocks[8].y -= step
        # Fifth block
        self.blocks[9].y += step
        # Fifth block
        self.blocks[10].x += step
        # Fifth block
        self.blocks[11].x += step
        self.blocks[11].y -= step


def draw_screen():
    """
    Функция отрисовки всей игровой области.
    """
    INFO_AREA1.draw()
    INFO_AREA2.draw()
    GAME_AREA1.draw()
    GAME_AREA2.draw()
    SEPARATING_LINE.draw()
    pygame.draw.line(SCREEN, SEPARATING_LINE1['color'], SEPARATING_LINE1['start'], SEPARATING_LINE1['stop'],
                     separate_line_width)
    pygame.draw.line(SCREEN, SEPARATING_LINE2['color'], SEPARATING_LINE2['start'], SEPARATING_LINE2['stop'],
                     separate_line_width)
    pygame.draw.line(SCREEN, SEPARATING_LINE3['color'], SEPARATING_LINE3['start'], SEPARATING_LINE3['stop'],
                     separate_line_width)
    pygame.draw.line(SCREEN, SEPARATING_LINE4['color'], SEPARATING_LINE4['start'], SEPARATING_LINE4['stop'],
                     separate_line_width)


def draw_figure(fig):
    for fig_block in fig.blocks:
        fig_block.draw()


def draw_next_figure(fig1, fig2):
    q_f = pygame.font.Font(None, 100)
    q_text = q_f.render('?', True, colors.TEXT)

    copy_figure1 = copy.deepcopy(fig1)
    if type(fig1) != DarkFigure1:
        for copy_block1 in copy_figure1.blocks:
            copy_block1.x = copy_block1.x - copy_figure1.x + 1.5
            copy_block1.y += 0.7
            copy_block1.draw()
    else:
        SCREEN.blit(q_text, (50, 30))

    copy_figure2 = copy.deepcopy(fig2)
    if type(fig2) != DarkFigure1:
        for copy_block2 in copy_figure2.blocks:
            copy_block2.x = WIDTH_SCREEN - info_area_width + copy_block2.x - copy_figure2.x + 1.5
            copy_block2.y += 0.7
            copy_block2.draw()
    else:
        SCREEN.blit(q_text, (WIDTH_SCREEN * Block.WIDTH - 100, 30))


def fall_figure(fig):
    """
    Функция движения фигур вниз
    """
    for fig_block in fig.blocks:
        fig_block.y += 1


def impact_figure(fig, free_blocks):
    """
    Функция проверки взаимодействия фигуры с одиночными блоками внизу. Если фигура
    "встала" на какой-либо блок или на дно игровой области, то возвращается True, в противном случае False
    """
    for fig_block in fig.blocks:
        if HEIGHT_SCREEN - fig_block.y == 1:
            return True
        for free_block in free_blocks:
            if free_block.y - fig_block.y == 1:
                if free_block.x == fig_block.x:
                    return True
    return False


def move_figure(fig, free_blocks, direction, area):
    if direction == 'RIGHT':
        step_block = 1
        # Проверка на столкновение со свободными блоками
        for fig_block in fig.blocks:
            for free_block in free_blocks:
                if fig_block.y == free_block.y:
                    if free_block.x - fig_block.x == step_block:
                        return  # Завершение функции, переиестить фигуру не удастся
        # Проверка на столкновение с границами игровой области
        for fig_block in fig.blocks:
            if fig_block.x == area.x + area.width - 1:
                return  # Завершение функции, переиестить фигуру не удастся
        # Перемещение фигуры возможно
        for fig_block in fig.blocks:
            fig_block.x += step_block

    if direction == 'LEFT':
        step_block = -1
        # Проверка на столкновение со свободными блоками
        for fig_block in fig.blocks:
            for free_block in free_blocks:
                if fig_block.y == free_block.y:
                    if free_block.x - fig_block.x == step_block:
                        return  # Завершение функции, переестить фигуру не удастся
        # Проверка на столкновение с границами игровой области
        for fig_block in fig.blocks:
            if fig_block.x == area.x:
                return  # Завершение функции, переиестить фигуру не удастся
        # Перемещение фигуры возможно
        for fig_block in fig.blocks:
            fig_block.x += step_block


def destroy_level(free_blocks, area):
    n_lvl = 0
    for i in range(1, area.height):
        # Находим количество блоков на каждом уровне
        level = []
        for free_block in free_blocks:
            if free_block.y == i:
                level.append(free_block)
        # Если какой-то уровень заполнен полностью
        if len(level) == area.width:
            n_lvl += 1
            # Удаляем все блоки уровня
            for kill_block in level:
                free_blocks.remove(kill_block)
            # Перемещаем все блоки, расположенные выше, вниз
            for free_block in free_blocks:
                if free_block.y < i:
                    free_block.y += 1
    if n_lvl >= 2:
        if area == GAME_AREA1:
            give_block(single_blocks2, GAME_AREA2, n_lvl)
        elif area == GAME_AREA2:
            give_block(single_blocks1, GAME_AREA1, n_lvl)


def give_block(free_blocks, area, n_lvl):
    """
    Функция добавления блоков противнику
    """
    global next_figure1, next_figure2
    if n_lvl == 2:
        # Поднимаем все блоки на 1 уровень
        for free_block in free_blocks:
            free_block.y -= 1
        # Рандомно создаём новый уровень из белых блоков
        list_x = []
        for i in range(area.width - 3):
            x = random.randint(area.x, area.x + area.width - 1)
            if x not in list_x:
                list_x.append(x)
        for x in list_x:
            white_block = Block(x, area.height - 1, colors.WHITE_BLOCKS)    # Создаём белые блоки
            free_blocks.append(white_block)
    elif n_lvl == 3:
        # Поднимаем все блоки на 2 уровня
        for free_block in free_blocks:
            free_block.y -= 2
        # Рандомно создаём 2 новых уровня из белых блоков
        list_x = []
        for i in range(area.width * 2 - 5):
            x = random.randint(area.x, area.x + area.width - 1)
            y = random.randint(area.height - 2, area.height - 1)
            if (x, y) not in list_x:
                list_x.append((x, y))
        for coord in list_x:
            white_block = Block(coord[0], coord[1], colors.WHITE_BLOCKS)  # Создаём белые блоки
            free_blocks.append(white_block)
    elif n_lvl == 4:
        chance = random.randint(1, 4)
        # Вариант 1
        if chance == 1:
            # Рандомно удаляем 7 столбцов на поле
            list_x = []
            for i in range(8):
                x = random.randint(0, area.width + 1)
                if x not in list_x:
                    list_x.append(x)
            for free_block in free_blocks:
                for x in list_x:
                    if free_block.x == x:
                        free_blocks.remove(free_block)
        # Вариант 2
        elif chance == 2:
            # Добавляет 3 слоя блоков в самый низ
            for free_block in free_blocks:  # Поднимаем все блоки на 2 уровня
                free_block.y -= 3
            # Рандомно создаём 2 новых уровня из белых блоков
            list_x = []
            for i in range(area.width * 3 - 7):
                x = random.randint(area.x, area.x + area.width - 1)
                y = random.randint(area.height - 3, area.height - 1)
                if (x, y) not in list_x:
                    list_x.append((x, y))
            for coord in list_x:
                white_block = Block(coord[0], coord[1], colors.WHITE_BLOCKS)  # Создаём белые блоки
                free_blocks.append(white_block)
        # Вариант 3
        else:
            # Создаём говноугольник
            if free_blocks == single_blocks1:
                next_figure1 = DarkFigure1(area.x + area.width // 2, 1)
            elif free_blocks == single_blocks2:
                next_figure2 = DarkFigure1(area.x + area.width // 2, 1)


def lose_game():
    loss = False
    f_game = pygame.font.Font(None, 40)
    text1 = f_game.render('Ты победил!', True, colors.TEXT)
    text2 = f_game.render('Ты проиграл!', True, colors.TEXT)
    loser = 0

    for free_block1 in single_blocks1:
        if free_block1.y <= 1:
            if free_block1.x <= GAME_AREA1.x + GAME_AREA1.width - 4 or free_block1.x >= GAME_AREA1.x + 3:
                loser = 1
    for free_block2 in single_blocks2:
        if free_block2.y <= 1:
            if free_block2.x <= GAME_AREA2.x + GAME_AREA2.width - 4 or free_block2.x >= GAME_AREA2.x + 3:
                loser = 2
    if loser == 1:
        # Отрисовка экрана концовки
        SCREEN.fill(colors.GRAY)
        pygame.draw.line(SCREEN, colors.SEPARATING_LINE, (WIDTH_SCREEN * Block.WIDTH // 2, 0),
                         (WIDTH_SCREEN * Block.WIDTH // 2, HEIGHT_SCREEN * Block.WIDTH),
                         width=Block.WIDTH)
        SCREEN.blit(text2, (70, 50))
        SCREEN.blit(text1, (WIDTH_SCREEN * Block.WIDTH - 290, 50))
        loss = True
    elif loser == 2:
        # Отрисовка экрана концовки
        SCREEN.fill(colors.GRAY)
        pygame.draw.line(SCREEN, colors.SEPARATING_LINE, (WIDTH_SCREEN * Block.WIDTH // 2, 0),
                         (WIDTH_SCREEN * Block.WIDTH // 2, HEIGHT_SCREEN * Block.WIDTH),
                         width=Block.WIDTH)
        SCREEN.blit(text1, (70, 50))
        SCREEN.blit(text2, (WIDTH_SCREEN * Block.WIDTH - 290, 50))
        loss = True
    return loss


def rotate(fig, free_blocks, area):
    """
    Функция поворота фигуры
    """
    # Устанавливаем значение шага блоков
    step_block = 1
    if fig.state == 1 or fig.state == 2:
        step_block = 1
    elif fig.state == 3 or fig.state == 4:
        step_block = -1
    copy_fig = copy.deepcopy(fig)  # Создаём копию фигуры

    possible_rotate = True  # Возможность развернуть фигуру
    if fig.state == 1 or fig.state == 3:
        copy_fig.rotate1(step_block)    # Поворачиваем копию фигуры
    elif fig.state == 2 or fig.state == 4:
        copy_fig.rotate2(step_block)  # Поворачиваем копию фигуры

    # Проверка пересечения single_blocks и блоков копии фигуры
    for fig_block in copy_fig.blocks:
        if possible_rotate:
            for free_block in free_blocks:
                if free_block.x == fig_block.x and free_block.y == fig_block.y:
                    possible_rotate = False
                    break   # Выход из цикла, чтобы не перебирать множество блоков без необходимости
        else:
            break   # Выход из цикла, чтобы не перебирать множество блоков без необходимости
    for fig_block in copy_fig.blocks:
        if fig_block.x < area.x or fig_block.x > area.x + area.width - 1:
            possible_rotate = False
            break  # Выход из цикла, чтобы не перебирать множество блоков без необходимости

    # Вызываем нужную функцию в зависимости от состояния фигуры
    if possible_rotate:
        if fig.state == 1 or fig.state == 3:
            if fig.state == 1:
                fig.state = 2
            elif fig.state == 3:
                fig.state = 4
            fig.rotate1(step_block)
        elif fig.state == 2 or fig.state == 4:
            if fig.state == 2:
                fig.state = 3
            elif fig.state == 4:
                fig.state = 1
            fig.rotate2(step_block)


# Создание игрового поля
info_area_width = 5   # Ширина инфообласти
game_area_width = 14   # Ширина игровой области
separate_line_width = 2     # Ширина центральной разделительной линии, ЗАДАНА В ПИКСЕЛЯХ

INFO_AREA1 = Area(0, 0, info_area_width, HEIGHT_SCREEN, colors.INFO_AREA)
SEPARATING_LINE1 = {'start': (info_area_width * Block.WIDTH - separate_line_width, 0),
                    'stop': (info_area_width * Block.WIDTH - separate_line_width, HEIGHT_SCREEN * Block.WIDTH),
                    'color': colors.SEPARATING_LINE}
GAME_AREA1 = Area(info_area_width, 0, game_area_width, HEIGHT_SCREEN, colors.GAME_AREA)
SEPARATING_LINE2 = {'start': ((info_area_width + game_area_width) * Block.WIDTH, 0),
                    'stop': ((info_area_width + game_area_width) * Block.WIDTH, HEIGHT_SCREEN * Block.WIDTH),
                    'color': colors.SEPARATING_LINE}
SEPARATING_LINE = Area(info_area_width + game_area_width, 0, 1, HEIGHT_SCREEN, colors.GRAY)
SEPARATING_LINE3 = {'start': ((WIDTH_SCREEN - info_area_width - game_area_width) * Block.WIDTH - separate_line_width,
                              0),
                    'stop': ((WIDTH_SCREEN - info_area_width - game_area_width) * Block.WIDTH - separate_line_width,
                             HEIGHT_SCREEN * Block.WIDTH),
                    'color': colors.SEPARATING_LINE}
GAME_AREA2 = Area(WIDTH_SCREEN - info_area_width - game_area_width, 0, game_area_width,
                  HEIGHT_SCREEN, colors.GAME_AREA)
SEPARATING_LINE4 = {'start': ((WIDTH_SCREEN - info_area_width) * Block.WIDTH, 0),
                    'stop': ((WIDTH_SCREEN - info_area_width) * Block.WIDTH, HEIGHT_SCREEN * Block.WIDTH),
                    'color': colors.SEPARATING_LINE}
INFO_AREA2 = Area(WIDTH_SCREEN - info_area_width, 0, info_area_width, HEIGHT_SCREEN, colors.INFO_AREA)


# Надписи на инфополе
f = pygame.font.Font(None, 20)
text = f.render('Следующая фигура:', True, colors.TEXT)


# Процесс создания фигур
"""figures = [OrangeFigure, OrangeFigure, OrangeFigure, BlueFigure, BlueFigure, BlueFigure, BlueFigure, GreenFigure,
           GreenFigure, GreenFigure, GreenFigure, RedFigure, RedFigure, RedFigure, RedFigure, AquaFigure, AquaFigure,
           AquaFigure, AquaFigure, PinkFigure, PinkFigure, PinkFigure, PinkFigure, YellowFigure, YellowFigure,
           YellowFigure, YellowFigure, PurpleFigure, DarkGreenFigure, LavenderFigure,
           KhakiFigure, MaroonFigure]"""

figures = [OrangeFigure, OrangeFigure, OrangeFigure, BlueFigure, BlueFigure, BlueFigure, BlueFigure, GreenFigure,
           GreenFigure, GreenFigure, GreenFigure, RedFigure, RedFigure, RedFigure, RedFigure, AquaFigure, AquaFigure,
           AquaFigure, AquaFigure, PinkFigure, PinkFigure, PinkFigure, PinkFigure, YellowFigure, YellowFigure,
           YellowFigure, YellowFigure]

# Стартовые фигуры
# figure1 = random.choice(figures)(GAME_AREA1.x + GAME_AREA1.width // 2, 1)
figure1 = DarkFigure1(GAME_AREA1.x + GAME_AREA1.width // 2, 1)
figure2 = random.choice(figures)(GAME_AREA2.x + GAME_AREA2.width // 2, 1)
next_figure1 = random.choice(figures)(GAME_AREA1.x + GAME_AREA2.width // 2, 1)
next_figure2 = random.choice(figures)(GAME_AREA2.x + GAME_AREA2.width // 2, 1)


# Одиночные блоки
single_blocks1 = []
single_blocks2 = []

# Новое движение фигур
motion1 = False
motion2 = False


# Переменная fall отвечает за движение фигуры вниз. На каждом игровом цикле ей добавляется 1.
# Если значение переменной fall делится без остатка на 70, фигуры делают шаг вниз.
fall1 = 0
fall2 = 0
running = True
while running:
    # Обработка событий
    for events in pygame.event.get():

        # Выход
        if events.type == pygame.QUIT:
            running = False

        # Поворот фигуры1
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_w:
                rotate(figure1, single_blocks1, GAME_AREA1)
            if events.key == pygame.K_d:
                move_figure(figure1, single_blocks1, 'RIGHT', GAME_AREA1)
            elif events.key == pygame.K_a:
                move_figure(figure1, single_blocks1, 'LEFT', GAME_AREA1)
            elif events.key == pygame.K_s:
                if not impact_figure(figure1, single_blocks1):
                    motion1 = True
                    # fall_figure(figure1)
        # Если кнопка отпущена
        elif events.type == pygame.KEYUP:
            if events.key == pygame.K_s:
                if not impact_figure(figure1, single_blocks1):
                    motion1 = False

        # Поворот фигуры2
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_UP:
                rotate(figure2, single_blocks2, GAME_AREA2)
            if events.key == pygame.K_RIGHT:
                move_figure(figure2, single_blocks2, 'RIGHT', GAME_AREA2)
            elif events.key == pygame.K_LEFT:
                move_figure(figure2, single_blocks2, 'LEFT', GAME_AREA2)
            elif events.key == pygame.K_DOWN:
                if not impact_figure(figure2, single_blocks2):
                    motion2 = True
                    # fall_figure(figure2)
        # Если кнопка отпущена
        elif events.type == pygame.KEYUP:
            if events.key == pygame.K_DOWN:
                if not impact_figure(figure2, single_blocks2):
                    motion2 = False

    if motion1:
        fall_figure(figure1)
    if motion2:
        fall_figure(figure2)

    if motion2:
        if motion2 == 'RIGHT':
            move_figure(figure2, single_blocks2, 'RIGHT', GAME_AREA2)
        elif motion2 == 'LEFT':
            move_figure(figure2, single_blocks2, 'LEFT', GAME_AREA2)

    # Уничтожение заполненных уровней
    destroy_level(single_blocks1, GAME_AREA1)
    destroy_level(single_blocks2, GAME_AREA2)

    # Процесс создания, движения и столкновения фигур
    fall1 += 1
    fall2 += 1
    if impact_figure(figure1, single_blocks1):
        # Добавление блоков фигуры в single_block
        for block in figure1.blocks:
            single_blocks1.append(block)
        figure1 = next_figure1
        next_figure1 = random.choice(figures)(GAME_AREA1.x + GAME_AREA1.width // 2, 1)
    else:
        if fall1 % 70 == 0:
            fall_figure(figure1)

    if impact_figure(figure2, single_blocks2):
        # Добавление блоков фигуры в single_block
        for block in figure2.blocks:
            single_blocks2.append(block)
        figure2 = next_figure2
        next_figure2 = random.choice(figures)(GAME_AREA2.x + GAME_AREA2.width // 2, 1)
    else:
        if fall2 % 70 == 0:
            fall_figure(figure2)

    # Отрисовка
    draw_screen()

    # Отрисовка текста на инфополе
    SCREEN.blit(text, (5, 5))
    SCREEN.blit(text, (INFO_AREA2.x * Block.WIDTH + 5, 5))

    # Отрисовка одиночных блоков
    for block in single_blocks1:
        block.draw()
    for block in single_blocks2:
        block.draw()

    # Отрисовка фигур
    draw_next_figure(next_figure1, next_figure2)
    draw_figure(figure1)
    draw_figure(figure2)

    if lose_game():     # Проверка на поражение одного из игроков
        pygame.display.update()
        clock.tick(FPS)
        time.sleep(3)
        running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
