import os

import pygame
from config import *
from create_map import Map

# TODO: Реализовать Столкновения


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if player is None:
                new_player = Player(0, 0)
            if level[y][x] == 0:
                Tile('water', x, y)
            elif level[y][x] == 1:
                Tile('cobblestone', x, y)
            elif level[y][x] == 2:
                Tile('grass', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode(SIZE)
player = None


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


class Tile(pygame.sprite.Sprite):
    title_images = {
        "grass": load_image("Textures", "Cobblestone.png"),
        "cobblestone": load_image("Textures", "grass.png"),
        "water": load_image("Textures", "Water.png")
    }

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = Tile.title_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image("Entity/Player", "Player.png")
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        camera.dx -= tile_width * x
        camera.dy -= tile_height * y
        self.pos = (x, y)
        for sprite in all_sprites:
            camera.apply(sprite)


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


if __name__ == '__main__':
    gameMap = Map()
    camera = Camera()
    player, level_x, level_y = generate_level(gameMap.genMap())
    camera.update(player)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                x, y = player.pos
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