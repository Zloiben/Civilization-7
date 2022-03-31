from __future__ import annotations

import os
import sys

import pygame

from config import *
from create_map import Map
from random import randint
from exceptions import *

# Задачи:
# -------------------------------------------------Сложные--------------------------------------------------------------

# TODO: Реализовать ратушу
# TODO: Реализовать экономику
# TODO: Реализовать разные классы героя
# TODO: Реализовать войско
# TODO: Реализовать столкновение 2.0
# -------------------------------------------------Средние--------------------------------------------------------------
# TODO: Реализовать настройки в которых можно изменить размер мира и тд
# --------------------------------------------------Легкие--------------------------------------------------------------
# TODO: Изменить Класс Map для внедрения в настройки
# ------------------------------------------------Неизвестно------------------------------------------------------------
# TODO: Реализвавать систуму добычи ресурсов
#  При создании мера одновремменно с этим делать карту ресуров на которой будет отображаться количиство ходов до конца
#  жилы. Пример рис1

# -------------------------------------------Возможные идеи-------------------------------------------------------------

# 1. Заменить рандомную генирацию мира на сид

# ----------------------------------------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode(SIZE)

player = False
Music = True


# -------------------------Функции для отображения уровня и загрузки текстур--------------------------------------------


def create_map(level):
    global player
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 0:
                TileType(0, x, y)
            elif level[y][x] == 2:
                TileType(2, x, y)
            elif level[y][x] == 1:
                TileType(1, x, y)
                if player is False and randint(0, 100) < 80:
                    player = Player(x, y)
    Start_Ui()
    # вернем игрока, а также размер поля в клетках
    return player, x, y


def load_map():
    """
    Функция будет реализованно в будущем, будет нужна для загрузки сохраненного мира
    """
    pass


def save_map():
    """
    Функция будет реализованна в будущем, будет нужна для сохранения мира
    """
    pass


def load_image(images_data, name, color_key=None):
    fullname = os.path.join(f'data/images/{images_data}/', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)

    image = image.convert_alpha()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    return image


def terminate():
    pygame.quit()
    sys.exit()


text = [(0, "Настройки."),
        (0, "<- Назад"),
        (1, "Музыка")]


def Start_Ui():
    UiSprite(load_image("Ui", "Next_Tern_Button.png"), WIDTH - 144, HEIGHT - 144)


def draw_settings_screen():
    fon = pygame.transform.scale(load_image("Menu", 'settings.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in text:
        if line[0] == 0:
            string_rendered = font.render(line[1], 1, pygame.Color('white'))
        else:
            string_rendered = font.render(line[1], 1, pygame.Color('Green'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        print(intro_rect)
        screen.blit(string_rendered, intro_rect)


def settings_screen():
    global Music
    draw_settings_screen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] in range(90, 110):
                    draw_start_screen()
                    return
                elif event.pos[1] in range(120, 140):
                    if text[2][0] == 1:
                        text[2] = (0, "Музыка")
                        Music = False
                    else:
                        text[2] = (1, "Музыка")
                        Music = True
                    draw_settings_screen()
        pygame.display.flip()


def draw_start_screen():
    intro_text = ["Начать игру",
                  "Настройки"]

    fon = pygame.transform.scale(load_image("Menu", 'fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        print(text_coord)
        screen.blit(string_rendered, intro_rect)


def start_screen():
    draw_start_screen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if event.pos[1] in range(90, 110):
                    settings_screen()
                else:
                    return  # начинаем игру
        pygame.display.flip()


start_screen()

if Music:
    pygame.mixer.music.load("data/sounds/fon.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(FON_VOLUME)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


# -----------------------------------------Дополнительные функции-------------------------------------------------------
# TODO: Будут реализованны в будущем

def get_camera_cell(mouse_position):
    """Определяет клетку которая, находится в камере"""
    print(((HEIGHT % tile_height) // 2) + tile_height / 2)
    x = int((mouse_position[0] - ((WIDTH % tile_width) // 2) + tile_width / 2) // tile_width)
    y = int((mouse_position[1] - ((HEIGHT % tile_height) // 2) + tile_height / 2) // tile_height)
    print(x, y)
    return x, y


def global_call(player_, mouse_position):
    local_x_pos, local_y_pos = get_camera_cell(mouse_position)
    """Определяет глобальную клетку по позицию игрока"""
    player_position_x, player_position_y = player_.pos
    global_cell_x = local_x_pos + player_position_x - (WIDTH // tile_width) // 2
    global_cell_y = local_y_pos + player_position_y - (HEIGHT // tile_height) // 2

    print(f" x: {global_cell_x}, y: {global_cell_y}")
    print(player_position_x, player_position_y)
    return global_cell_x, global_cell_y


def get_sprite(x, y):
    return tiles_type_group.sprites()[100 * y + x]


def buildTerr(player_, mouse_position):
    global_cell_x, global_cell_y = global_call(player_, mouse_position)
    get_sprite(global_cell_x, global_cell_y).change_type(1)


def buildWat(player_, mouse_position):
    global_cell_x, global_cell_y = global_call(player_, mouse_position)
    get_sprite(global_cell_x, global_cell_y).change_type(0)

# -----------------------------------------Сущности---------------------------------------------------------------------


class Entity:
    """
    Класс от которого наследуется все существа
    """

    range_attacks_data = {
        "nearby": 50,
        "average": 75,
        "far": 100,
        "very far": 250
    }

    def __init__(self, hp: int | float, damage: int | float, step: int, range_attack: str, pos_x: int, pos_y: int):
        self.hp = hp
        self.range_attack = Entity.range_attacks_data[range_attack]
        self.range_attack_name = range_attack
        self.damage = damage
        self.step = step
        self.MAX_STEPS = step
        self.pos = pos_x, pos_y

    def __str__(self):
        return f"""
        {"-" * 200}
        Информация о сущности - {self.__class__.__name__}
        Количество здоровья: {self.hp}
        Дальность атаки: {self.range_attack} / {self.range_attack_name}
        Урон: {self.damage}
        Осталось шагов в этом ходу: {self.step}
        Максимальное количество шагов: {self.MAX_STEPS}
        {"-" * 200}
        """

    def get_hp(self) -> int | float: return self.hp

    def get_damage(self) -> int | float: return self.damage

    def get_step(self) -> int: return self.step

    def attack(self, entity: Entity): entity.hp -= self.damage

    def new_motion(self): self.step = self.MAX_STEPS

    def set_pos(self, x: int, y: int): self.pos = (x, y)

    def set_hp(self, hp: int | float): self.hp = hp

    def set_damage(self, damage: int | float): self.damage = damage

    def set_step(self, step: int): self.step = step

    def set_max_steps(self, step: int): self.MAX_STEPS = step

    def set_range_attack(self, range_attack: str): self.range_attack = Entity.range_attacks_data[range_attack]

    # -------------------------------------------Тестовые функции------------------------------------------------------


class Player(Entity, pygame.sprite.Sprite):
    """Главный персонаж"""

    def __init__(self, pos_x: int, pos_y: int):
        super(Player, self).__init__(100, 15, 10, "nearby", pos_x, pos_y)
        super(Entity, self).__init__(player_group, all_sprites)
        self.image = load_image("Entity/Player", "Hup.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# ------------------------------------------Буду реализованны в будущем-------------------------------------------------


class Knight(Entity, pygame.sprite.Sprite):
    """Рыцарь"""

    def __init__(self, pos_x, pos_y):
        super(Knight, self).__init__(250, 30, 5, "average", pos_x, pos_y)


class Archer(Entity, pygame.sprite.Sprite):
    """Лучник"""

    def __init__(self, pos_x, pos_y):
        super(Archer, self).__init__(80, 30, 5, "far", pos_x, pos_y)


# -------------------------Функции для игрока---------------------------------------------------------------------------


def move_check(player_: Player, direction: str):
    """Проверяет правильность совершаемого движения"""
    x, y = player_.pos
    if direction == "up":
        player_.image = load_image("Entity/Player", "Hback.png")
        if get_sprite(x, y - 1).type == 1:
            player_.set_pos(x, y - 1)
            player_.rect.y -= tile_height
    elif direction == "down":
        player_.image = load_image("Entity/Player", "Hup.png")
        if get_sprite(x, y + 1).type == 1:
            player_.set_pos(x, y + 1)
            player_.rect.y += tile_height
    elif direction == "left":
        player_.image = load_image("Entity/Player", "Hleft.png")
        if get_sprite(x - 1, y).type == 1:
            player_.set_pos(x - 1, y)
            player_.rect.x -= tile_width
    elif direction == "right":
        player_.image = load_image("Entity/Player", "Hright.png")
        if get_sprite(x + 1, y).type == 1:
            player_.set_pos(x + 1, y)
            player_.rect.x += tile_width
    else:
        raise DirectionError


# ---------------------------------------------Текстуры-----------------------------------------------------------------


class Tile:
    """Класс от которого будут наследоваться все текстуры"""
    tile_images = {
        "11": load_image("Textures", "Grass.png"),
        "12": load_image("Textures", "Grass_2.png"),
        "2": load_image("Textures", "Cobblestone.png"),
        "0": load_image("Textures", "Water.png")
    }

    def __init__(self, tile_type: str, pos_x: int, pos_y: int):
        self.image = Tile.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def change_type(self, type_int):
        pass


class TileType(Tile, pygame.sprite.Sprite):
    """Спрайты через которые можно проходить"""

    def __init__(self, type_int, pos_x, pos_y):
        self.type = type_int
        if self.type == 1:
            type_int = str(self.type) + str(randint(1, 2))
        super(TileType, self).__init__(str(type_int), pos_x, pos_y)
        super(Tile, self).__init__(tiles_type_group, all_sprites)

    def change_type(self, type_int):
        self.type = type_int
        if self.type == 1:
            type_int = str(self.type) + str(randint(1, 2))
        self.image = Tile.tile_images[str(type_int)]


class TileClose(Tile, pygame.sprite.Sprite):
    """Спрайты через которые нельзя проходить"""

    def __init__(self, tile_type, pos_x, pos_y):
        super(TileClose, self).__init__(tile_type, pos_x, pos_y)
        super(Tile, self).__init__(tiles_close_group, all_sprites)


class UiSprite(pygame.sprite.Sprite):
    """Спрайты через которые нельзя проходить"""

    def __init__(self, img, pos_x, pos_y):
        self.image = img
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        super(UiSprite, self).__init__(ui_sprites_group)


# ---------------------------------------------Здания-------------------------------------------------------------------


class Building:
    """Класс от которого будут наследоваться все здания"""

    def __init__(self):
        pass


# ----------------------------------------------------------------------------------------------------------------------


all_sprites = pygame.sprite.Group()
tiles_type_group = pygame.sprite.Group()  # Спрайты через которые можно проходить
ui_sprites_group = pygame.sprite.Group()  # Спрайты Ui
tiles_close_group = pygame.sprite.Group()  # Спрайты через которые нельзя проходить
player_group = pygame.sprite.Group()

clock = pygame.time.Clock()

gameMap = Map()
camera = Camera()
map_data = gameMap.generation_map()
player, level_x, level_y = create_map(map_data)
camera.update(player)
for sprite in all_sprites:
    camera.apply(sprite)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                move_check(player, "up")
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                move_check(player, "down")
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                move_check(player, "left")
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                move_check(player, "right")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                buildTerr(player, pygame.mouse.get_pos())
            if event.button == 3:
                buildWat(player, pygame.mouse.get_pos())
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    player_group.draw(screen)
    ui_sprites_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
