
import random


class Cell:
    def __init__(self):
        self.type = 1
        self.build = 0

    def __str__(self): return f"Cell: {self.type}, {self.build}"

    def get_type(self) -> int: return self.type  # Возражает тип клетки

    def get_object(self) -> int: return self.build  # Возражает обьект на клетке

    def set_type(self, type_sprite: int): self.type = type_sprite  # Изменяет тип

    def set_object(self, obj: int): self.build = obj  # Изменяет обьект на клетке


class Map:
    def __init__(self):
        self.map = [[Cell() for _ in range(100)] for _ in range(100)]
        self.typeImg = {0: "~", 1: "█", 2: "↑"}

    def __str__(self): return self.map

    def get_type(self, x: int, y: int) -> int: return self.map[y][x].get_type()  # Возражает тип клетки

    def get_object(self, x: int, y: int) -> int: return self.map[y][x].get_object()  # Возражает что стоит на клетке

    def set_type(self, x: int, y: int, type_cell: int): self.map[y][x].set_type(type_cell)  # Изменяет клетку

    def set_object(self, x: int, y: int, object_type: int):  self.map[y][x].set_object(object_type)  # Изменяет объект

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
                        if ra >= (pr - 3) * 20:
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
        print("Hills generation: Done")

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


if __name__ == "__main__":
    gameMap = Map()
    gameMap.genMap()
    for i in range(len(gameMap.map)):
        for j in range(len(gameMap.map[0])):
            print(gameMap.map[i][j])
