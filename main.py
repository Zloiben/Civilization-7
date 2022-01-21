from __future__ import annotations

import os
import pygame

from config import *
from create_map import Map
from random import randint

# Задачи:
# Сложные
# TODO: Реализовать ратушу
# TODO: Реализовать экономику
# TODO: Реализовать разные классы героя
# TODO: Реализовать войско
# Средние
# Легкие
# TODO: Сделать чтобы игрок появлялся на земле
# TODO: Реализовать столкновения
# TODO: Сделать текстуры земли
# Неизвестно
# TODO: Изменить архитектуру
# TODO: Реализовать костыль хода

# Возможные идеи
# 1. Заменить рандомную генирацию мира на сид

pygame.init()
screen = pygame.display.set_mode(SIZE)
player = False

# -------------------------Функции для отображения уровня и загрузки текстур--------------------------------------------


def generate_map(level):
    global player
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 0:
                Tile('water', x, y)
            elif level[y][x] == 2:
                Tile('cobblestone', x, y)
            elif level[y][x] == 1:
                Tile('grass', x, y)
                if player is False and randint(0, 100) > 80:
                    player = Player(x, y)
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


# -----------------------------------------Сущности---------------------------------------------------------------------


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

    def __init__(self, hp: int | float, damage: int | float, step: int, range_attack: str):
        """
        :param hp: Здоровье
        :param damage: Урон
        :param step: Количество Шагов
        :param range_attack: Дальность атаки
        """
        self.hp = hp
        self.range_attack = Entity.range_attacks_data[range_attack]
        self.range_attack_name = range_attack
        self.damage = damage
        self.step = step
        self.MAX_STEPS = step

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

    def get_damage(self) -> int | float: return self.damage  # Возражает количество урона

    def get_step(self) -> int: return self.step  # Возражает Количество оставшихся шагов

    # Функции для взаимодействия ---------------------------------------------------------------------------------------

    def attack(self, entity: Entity): entity.hp -= self.damage  # Атакует указанное существо

    # Функции для логики сущности --------------------------------------------------------------------------------------

    def new_motion(self): self.step = self.MAX_STEPS  # Обновляет количество шагов после завершения хода

    def move(self):  # Ход
        self.step -= 1
        if self.step == 0:
            self.new_motion()

    # -------------------------------------------Функции для тестов-----------------------------------------------------

    def set_hp(self, hp: int | float): self.hp = hp

    def set_damage(self, damage: int | float): self.damage = damage

    def set_step(self, step: int): self.step = step

    def set_max_steps(self, step: int): self.MAX_STEPS = step

    def set_range_attack(self, range_attack: str): self.range_attack = Entity.range_attacks_data[range_attack]

    # -------------------------------------------Тестовые функции-------------------------------------------------------


class Player(Entity, pygame.sprite.Sprite):
    """Главный персонаж"""

    image = load_image("Entity/Player", "Hero.png")

    def __init__(self, pos_x, pos_y):
        super(Player, self).__init__(100, 15, 10, "nearby")
        super(Entity, self).__init__(player_group, all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


class Knight(Entity, pygame.sprite.Sprite):
    """Рыцарь"""

    def __init__(self):
        super(Knight, self).__init__(250, 30, 5, "average")


class Archer(Entity, pygame.sprite.Sprite):
    """Лучник"""

    def __init__(self):
        super(Archer, self).__init__(80, 30, 5, "far")

# ---------------------------------------------Текстуры-----------------------------------------------------------------


class Tile(pygame.sprite.Sprite):
    title_images = {
        "grass": load_image("Textures", "grass.png"),
        "cobblestone": load_image("Textures", "Cobblestone.png"),
        "water": load_image("Textures", "Water.png")
    }

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = Tile.title_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# ---------------------------------------------Здания-------------------------------------------------------------------

class Building:

    """Класс от которого будут наследоваться все здания"""

    def __init__(self):
        pass

# ----------------------------------------------------------------------------------------------------------------------


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

clock = pygame.time.Clock()


gameMap = Map()
camera = Camera()
player, level_x, level_y = generate_map(gameMap.genMap())
camera.update(player)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.rect.y -= 50
            elif event.key == pygame.K_DOWN:
                player.rect.y += 50
            elif event.key == pygame.K_LEFT:
                player.rect.x -= 50
            elif event.key == pygame.K_RIGHT:
                player.rect.x += 50

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    player_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()