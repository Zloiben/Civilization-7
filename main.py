from __future__ import annotations

import os

import pygame

from config import *
from create_map import Map
from random import randint
from exceptions import *
import random
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

# ----------------------------------------------Баги--------------------------------------------------------------------
# TODO: Налаживание текстур 
# ----------------------------------------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode(SIZE)
player = False

# -------------------------Функции для отображения уровня и загрузки текстур--------------------------------------------


class Cell:
    def __init__(self):
        self.type = 1
        self.build = 0
        self.resurses = 0

    def __str__(self): return f"Cell: {self.type}, {self.build}, {self,resurses}"

    def get_type(self) -> int: return self.type  # Возражает тип клетки

    def get_object(self) -> int: return self.build  # Возражает обьект на клетке
    
    def get_resurses(self) -> int: return self.resurses  # Возражает обьект на клетке

    def set_resurses(self, resurses: int): self.resurses = resurses  # Изменяет тип

    def set_type(self, type: int): self.type = type  # Изменяет тип

    def set_object(self, obj: int): self.build = obj  # Изменяет обьект на клетке


class Map:
    def __init__(self):
        self.map = [[Cell() for _ in range(100)] for _ in range(100)]
        self.typeImg = {0: "~", 1: "█", 2: "↑"}
        self.player_pos = (50, 50)
        self.render_map = Tile_map()
        self.render_map.update()
        self.render_map.draw
        
    def __str__(self): return self.map

    def get_type(self, x: int, y: int) -> int: return self.map[y][x].get_type()  # Возражает тип клетки

    def get_object(self, x: int, y: int) -> int: return self.map[y][x].get_object()  # Возражает что стоит на клетке

    def set_type(self, x: int, y: int, type_cell: int): self.map[y][x].set_type(type_cell)  # Изменяет клетку

    def set_object(self, x: int, y: int, object_type: int):  self.map[y][x].set_object(object_type)  # Изменяет объект

    def get_player_pos(self): self.player_pos  # Возражает позицию игрока

    def set_player_pos(self, x: int, y: int):  self.player_pos = (x, y)  # Изменяет позицию игрока
    
    def draw_tile_map(self): self.render_map.draw()
    
    def draw_tile_map(self): self.render_map.update()
    
    def generation_map(self, width: int = 100, height: int = 100):
        mp = [[0 for _ in range(width)] for _ in range(height)]

        for _ in range(10):
            mp[random.randint(20, 80)][random.randint(20, 80)] = 3
        pr = 3
        while True:
            for y in range(100):
                for x in range(100):
                    if mp[y][x] == pr:
                        mp[y][x] = 1
                        ra = random.randint(0, 100)
                        if ra >= (pr - 3) * 5:
                            if mp[y + 1][x] == 0:
                                mp[y + 1][x] = pr + 1
                            if mp[y - 1][x] == 0:
                                mp[y - 1][x] = pr + 1
                            if mp[y][x + 1] == 0:
                                mp[y][x + 1] = pr + 1
                            if mp[y][x - 1] == 0:
                                mp[y][x - 1] = pr + 1
            pr += 1
            f = True
            for i in mp:
                if pr in i:
                    f = False
            if f:
                break
        print("continental generation: Done")
        for i in range(20):
            x = random.randint(20, 80)
            y = random.randint(20, 80)
            while mp[x][y] != 1:
                x = random.randint(20, 80)
                y = random.randint(20, 80)
            mp[x][y] = 3
        pr = 3
        while True:
            for y in range(100):
                for x in range(100):
                    if mp[y][x] == pr:
                        mp[y][x] = 2
                        ra = random.randint(0, 100)
                        if ra >= (pr - 3) * 15:
                            if mp[y + 1][x] == 1:
                                mp[y + 1][x] = pr + 1
                            if mp[y - 1][x] == 1:
                                mp[y - 1][x] = pr + 1
                            if mp[y][x + 1] == 1:
                                mp[y][x + 1] = pr + 1
                            if mp[y][x - 1] == 1:
                                mp[y][x - 1] = pr + 1
            pr += 1
            f = True
            for i in mp:
                if pr in i:
                    f = False
            if f:
                break
        print("forest generation: Done")

        for i in range(100):
            for l in range(100):
                self.set_type(i, l, mp[l][i])
        self.set_type(0, 0, 2)
        self.set_type(0, 1, 1)
        drdic = {0:"~", 1:"█", 2:"↑"}
        for i in range(100):
            for l in range(100):
                print(drdic[mp[l][i]], end="")
            print()
        return mp



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
        fullname = os.path.join(f'data/images/Textures/error')
        image = pygame.image.load(fullname)
        raise

    image = image.convert_alpha()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    return image

# -----------------------------------------Дополнительные классы--------------------------------------------------------


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


def get_camera_cell(mouse_position):
    """Определяет клетку которая, находится в камере"""
    # x = int((mouse_position[0] - self.left) / self.cell_size)
    # y = int((mouse_position[1] - self.top) / self.cell_size)
    x = int(mouse_position[0] // tile_width)
    y = int(mouse_position[1] // tile_height)
    print(x, y)
    global_call(player, x, y)


def global_call(player_, mouse_position_x, mouse_position_y):
    """Определяет глобальную клетку по позицию игрока"""
    # TODO: в будущем нужно добавить чтобы учитывались еще несколько разных спрайтов из за наложения
    player_position_x, player_position_y = player_.pos

    global_cell_x = mouse_position_x
    global_cell_y = mouse_position_y

    print(f" x: {global_cell_x}, y: {global_cell_y}")
    print(player_position_x, player_position_y)
    test_global_cell(global_cell_x, global_cell_y)


def test_global_cell(global_cell_x, global_cell_y):
    map_data[global_cell_y][global_cell_x] = 2
    for i in all_sprites.sprites():
        print(i.rect)
    # TileClose("cobblestone", global_cell_x, global_cell_y)
    # tiles_close_group.add(TileClose("cobblestone", global_cell_x, global_cell_y))
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
    # -------------------------------------------Основные функции-------------------------------------------------------

    # Функции которые возвращают информацию о сущности -----------------------------------------------------------------

    def get_hp(self) -> int | float: return self.hp  # Возражает количество хп

    def get_damage(self) -> int | float: return self.damage  # Возражает наносимый урон

    def get_step(self) -> int: return self.step  # Возражает количество оставшихся шагов

    # Функции для взаимодействия ---------------------------------------------------------------------------------------

    def attack(self, entity: Entity): entity.hp -= self.damage  # Атакует указанное существо

    # Функции для логики сущности --------------------------------------------------------------------------------------

    def new_motion(self): self.step = self.MAX_STEPS  # Обновляет количество шагов после завершения хода

    def set_pos(self, x: int, y: int): self.pos = (x, y)

    # -------------------------------------------Функции для тестов-----------------------------------------------------

    def set_hp(self, hp: int | float): self.hp = hp  # Изменяет количество здоровья.

    def set_damage(self, damage: int | float): self.damage = damage  # Изменяет наносимый урон.

    def set_step(self, step: int): self.step = step  # Изменяет количество шагов.

    def set_max_steps(self, step: int): self.MAX_STEPS = step  # Изменяет максимальное количество шагов.

    # Изменяет дальность атаки
    def set_range_attack(self, range_attack: str): self.range_attack = Entity.range_attacks_data[range_attack]

    # -------------------------------------------Тестовые функции------------------------------------------------------


class Player(Entity, pygame.sprite.Sprite):
    """Главный персонаж"""

    image = load_image("Entity/Player", "Hero.png")

    def __init__(self, pos_x: int, pos_y: int):
        super(Player, self).__init__(100, 15, 10, "nearby", pos_x, pos_y)
        super(Entity, self).__init__(player_group, all_sprites)
        self.image = Player.image
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
        # if map_data[y - 1][x] != 0 and map_data[y - 1][x] != 2:
        player_.set_pos(x, y - 1)
        player_.rect.y -= tile_height
    elif direction == "down":
        # if map_data[y + 1][x] != 0 and map_data[y + 1][x] != 2:
        player_.set_pos(x, y + 1)
        player_.rect.y += tile_height
    elif direction == "left":
        # if map_data[y][x - 1] != 0 and map_data[y][x - 1] != 2:
        player_.set_pos(x - 1, y)
        player_.rect.x -= tile_width
    elif direction == "right":
        # if map_data[y][x + 1] != 0 and map_data[y][x + 1] != 2:
        player_.set_pos(x + 1, y)
        player_.rect.x += tile_width
    else:
        raise DirectionError


# ---------------------------------------------Текстуры-----------------------------------------------------------------

class Tile_map:
    """Класс создан для рендаринга карты по слоям. Через эту карту есть доступ к спрайтам, чтобы изменитять карту."""
        def __init__(self, gen_map: Map):
            self.map_1 = [[Tile("T", 0, x, y) for x in range(100)] for y in range(100)] #Карта типов клеток
            self.map_2 = [[Tile("R", 0, x, y) for x in range(100)] for y in range(100)] #Карта ресурсов
            self.map_3 = [[Tile("B", 0, x, y) for x in range(100)] for y in range(100)] #карта построек
            self.true_map = gen_map
            
            all_sprites = pygame.sprite.Group()
            lays_of_sprites = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()] 
            gg_sprites = pygame.sprite.Group()
            self.Hero = Hero(0, 0)
            #0 - спрайты карты типов
            #1 - спрайты карты ресурсов
            #2 - спрайты карты типы
            
        def update(self):
            """Приводит визуальную карту к текстовой."""
            #первый слой
            for y in range(100):
                for x in range(100):
                    self.map_1[y][x].change_image("T", self.true_map.get_type(x, y))
                    self.map_1[y][x].update()
            #второй слой
            for y in range(100):
                for x in range(100):
                    self.map_2[y][x].change_image("R", self.true_map.get_resurses(x, y))
                    self.map_1[y][x].update()
            #третий слой
            for y in range(100):
                for x in range(100):
                    self.map_3[y][x].change_image("B", self.true_map.get_object(x, y))
                    self.map_1[y][x].update()
            self.gg_sprites.update()
            self.draw()
        
        def draw(self):
                        """Рисует кадр"""
            self.map_1.draw(screen)
            self.map_2.draw(screen)
            self.map_3.draw(screen)
            self.gg_sprites.draw(screen)
            
            
class Tile(pygame.sprite.Sprite):
    """Класс от которого будут наследоваться все текстуры"""
    def __init__(self, tile_type: str, tile_num: str, pos_x: int, pos_y: int):
        pygame.sprite.__init__(self)
        dic = {"T": gameMap.tile_map.lays_of_sprites[0],
        "R": gameMap.tile_map.lays_of_sprites[1],
        "B": gameMap.tile_map.lays_of_sprites[2]}
        self.add(gameMap.all_sprites, dic)
        self.image = load_image("Textures", (tile_type) + (tile_num) + ".png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
    
    def change_image(self, tile_type, tile_num):
        elf.image = load_image("Textures", (tile_type) + (tile_num) + ".png")

class Hero(pygame.sprite.Sprite):
    """Класс от которого будут наследоваться все текстуры"""
    def __init__(self, , pos_x: int, pos_y: int):
        pygame.sprite.__init__(self)
        self.add(gameMap.all_sprites, gameMap.gg_sprites)
        self.image = load_image("Entity/Player", "Hero.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        
#class TileAvailable(Tile, pygame.sprite.Sprite):
#   """Спрайты через которые можно проходить"""
#
#    def __init__(self, tile_type, pos_x, pos_y):
#        super(TileAvailable, self).__init__(tile_type, pos_x, pos_y)
#        super(Tile, self).__init__(tiles_available_group, all_sprites)
#
#
#class TileClose(Tile, pygame.sprite.Sprite):
#    """Спрайты через которые нельзя проходить"""
#
#    def __init__(self, tile_type, pos_x, pos_y):
#        super(TileClose, self).__init__(tile_type, pos_x, pos_y)
#        super(Tile, self).__init__(tiles_close_group, all_sprites)


# ---------------------------------------------Здания-------------------------------------------------------------------


class Building:

    """Класс от которого будут наследоваться все здания"""

    def __init__(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------




clock = pygame.time.Clock()
gameMap = Map()
gameMap.genMap()
camera = Camera()
player, level_x, level_y = create_map(map_data)
camera.update(gameMap.render_map.map_1[gameMap.get_player_pos[0]]
    [gameMap.get_player_pos[1]])
for sprite in all_sprites:
    camera.apply(sprite)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            get_camera_cell(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                gameMap.set_player_pos(gameMap.get_player_pos[0],
                    gameMap.get_player_pos[1] - 1)
            elif event.key == pygame.K_DOWN:
                gameMap.set_player_pos(gameMap.get_player_pos[0],
                    gameMap.get_player_pos[1] + 1)
            elif event.key == pygame.K_LEFT:
                gameMap.set_player_pos(gameMap.get_player_pos[0] + 1,
                    gameMap.get_player_pos[1])
            elif event.key == pygame.K_RIGHT:
                gameMap.set_player_pos(gameMap.get_player_pos[0] - 1,
                    gameMap.get_player_pos[1] - 1)
            camera.update(gameMap.render_map.map_1[gameMap.get_player_pos[0]]
                [gameMap.get_player_pos[1]])
            for sprite in all_sprites:
                camera.apply(sprite)
    screen.fill(pygame.Color("black"))
    gameMap.draw()
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()

# Я Богдан. Ну я богом дан. Я приёмный сын пениса и сводный сын Валеры

