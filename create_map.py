
import random


class Cell:
    def __init__(self):
        self.space = 0
        self.type = 1
        self.build = 0

    def __str__(self):
        # для отладки
        return f"Cell: {self.type}, {self.build}, {self.space}"

    def getType(self):
        return self.type

    def getSpace(self):
        return self.space

    def getBuild(self):
        return self.build

    def setType(self, x):
        self.type = x

    def setSpace(self, x):
        self.space = x

    def setBuild(self, x):
        self.build = x


class Map:
    def __init__(self):
        self.map = [[Cell() for l in range(100)] for i in range(100)]
        self.typeImg = {0:"~", 1:"█", 2:"↑"}

    def __str__(self):
        return self.map

    def getCellType(self, x, y):
        return self.map[y][x].getType()

    def getCellSpace(self, x, y):
        return self.map[y][x].getSpace()

    def getCellBuild(self, x, y):
        return self.map[y][x].getBuild()

    def setCellType(self, x, y, t):
        self.map[y][x].setType(t)

    def setCellSpace(self, x, y, s):
        self.map[y][x].setSpace(s)

    def setCellBuild(self, x, y, b):
        self.map[y][x].setBuild(b)

    def updateMap(self):
        global screen
        for y in range(100):
            for x in range(100):
                screen.blit(self.typeImg[self.getCellType(x, y)],
                            (x * 64, y * 64))

    def genMap(self):
        mp = [[0 for _ in range(100)] for _ in range(100)]
        for i in range(10):
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
                self.setCellType(i, l, mp[l][i])
        self.setCellType(0, 0, 2)
        self.setCellType(0, 1, 1)
        drdic = {0:"~", 1:"█", 2:"↑"}
        for i in range(100):
            for l in range(100):
                print(drdic[mp[l][i]], end="")
            print()
        return mp
