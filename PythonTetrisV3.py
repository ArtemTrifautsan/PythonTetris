import pygame
import random
import colors   # Цвета в отдельном модуле
import copy
import time


pygame.init()

# Основные параметры
# 1 игровая область 420 пикселей и 1 инфообласть 150 пикселей
# Ширина и высота экрана выражена в блоках, помещающихся в экран, а не в пиксилях
WIDTH_SCREEN = 19
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
    GAME_AREA.draw()
    INFO_AREA.draw()
    pygame.draw.line(SCREEN, SEPARATING_LINE['color'], SEPARATING_LINE['start'], SEPARATING_LINE['stop'],
                     separate_line_width)


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


def fall_figure(fig):
    """
    Функция движения фигур вниз
    """
    for fig_block in fig.blocks:
        fig_block.y += 1


def draw_next_figure(fig):
    q_f = pygame.font.Font(None, 100)
    q_text = q_f.render('?', True, colors.TEXT)

    copy_figure = copy.deepcopy(fig)
    if type(fig) != DarkFigure1:
        for copy_block in copy_figure.blocks:
            copy_block.x = WIDTH_SCREEN - info_area_width + copy_block.x - copy_figure.x + 1.4
            copy_block.y += 0.7
            copy_block.draw()
    else:
        SCREEN.blit(q_text, (WIDTH_SCREEN * Block.WIDTH - 100, 30))


def draw_figure(fig):
    for fig_block in fig.blocks:
        fig_block.draw()


def lose_game():
    loss = False
    f_game = pygame.font.Font(None, 60)
    loss_text = f_game.render('Ты проиграл!', True, colors.TEXT)

    for free_block in single_blocks:
        if free_block.y <= 1:
            if free_block.x <= GAME_AREA.x + GAME_AREA.width - 4 or free_block.x >= GAME_AREA.x + 3:
                loss = True
    if loss:
        # Отрисовка экрана концовки
        SCREEN.fill(colors.GRAY)
        SCREEN.blit(loss_text, ((WIDTH_SCREEN * Block.WIDTH - 60) // 2, (HEIGHT_SCREEN * Block.WIDTH - 60) // 2))
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
    for i in range(1, area.height):
        # Находим количество блоков на каждом уровне
        level = []
        for free_block in free_blocks:
            if free_block.y == i:
                level.append(free_block)
        # Если какой-то уровень заполнен полностью
        if len(level) == area.width:
            # Удаляем все блоки уровня
            for kill_block in level:
                free_blocks.remove(kill_block)
            # Перемещаем все блоки, расположенные выше, вниз
            for free_block in free_blocks:
                if free_block.y < i:
                    free_block.y += 1


info_area_width = 5   # Ширина инфообласти
game_area_width = 14   # Ширина игровой области
separate_line_width = 2     # Ширина центральной разделительной линии, ЗАДАНА В ПИКСЕЛЯХ

GAME_AREA = Area(0, 0, game_area_width, HEIGHT_SCREEN, colors.GAME_AREA)
SEPARATING_LINE = {'start': (game_area_width * Block.WIDTH, 0),
                   'stop': (game_area_width * Block.WIDTH, HEIGHT_SCREEN * Block.WIDTH),
                   'color': colors.SEPARATING_LINE}
INFO_AREA = Area(game_area_width, 0, game_area_width + info_area_width, HEIGHT_SCREEN, colors.INFO_AREA)


# Надписи на инфополе
f = pygame.font.Font(None, 22)
text = f.render('Следующая фигура:', True, colors.TEXT)


# Процесс создания фигур
figures = [OrangeFigure, BlueFigure, GreenFigure, RedFigure, AquaFigure, PinkFigure, YellowFigure, DarkGreenFigure,
           PurpleFigure, LavenderFigure, KhakiFigure, MaroonFigure]

# Стартовые фигуры
figure = random.choice(figures)(GAME_AREA.x + GAME_AREA.width // 2, 1)
next_figure = random.choice(figures)(GAME_AREA.x + GAME_AREA.width // 2, 1)
# С шансом 1% может попасться говноугольник
chance = random.randint(0, 100)
if chance == 57:
    next_figure = DarkFigure1(GAME_AREA.x + GAME_AREA.width // 2, 1)


# Одиночные блоки
single_blocks = []


fall = 0
running = True
while running:
    # Обработка событий
    for events in pygame.event.get():

        # Выход
        if events.type == pygame.QUIT:
            running = False

        # Поворот фигуры
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_UP:
                rotate(figure, single_blocks, GAME_AREA)
            if events.key == pygame.K_RIGHT:
                move_figure(figure, single_blocks, 'RIGHT', GAME_AREA)
            elif events.key == pygame.K_LEFT:
                move_figure(figure, single_blocks, 'LEFT', GAME_AREA)
            elif events.key == pygame.K_DOWN:
                if not impact_figure(figure, single_blocks):
                    fall_figure(figure)

    # Уничтожение заполненных уровней
    destroy_level(single_blocks, GAME_AREA)

    # Процесс создания, движения и столкновения фигур
    fall += 1
    if impact_figure(figure, single_blocks):
        # Добавление блоков фигуры в single_block
        for block in figure.blocks:
            single_blocks.append(block)
        figure = next_figure
        next_figure = random.choice(figures)(GAME_AREA.x + GAME_AREA.width // 2, 1)
        chance = random.randint(0, 100)
        if chance == 57:
            next_figure = DarkFigure1(GAME_AREA.x + GAME_AREA.width // 2, 1)
    else:
        if fall % 35 == 0:
            fall_figure(figure)

    # Отрисовка
    draw_screen()

    # Отрисовка текста на инфополе
    SCREEN.blit(text, (INFO_AREA.x * Block.WIDTH + 5, 5))

    # Отрисовка одиночных блоков
    for block in single_blocks:
        block.draw()

    # Отрисовка фигур
    draw_next_figure(next_figure)
    draw_figure(figure)

    if lose_game():     # Проверка на поражение одного из игроков
        pygame.display.update()
        clock.tick(FPS)
        time.sleep(3)
        running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
