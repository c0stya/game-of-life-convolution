import random


class Cell(object):
    def __init__(self, x, y, val, field):
        self.x, self.y = x, y
        self.val = val
        self.field = field

    def get_new_value(self):
        neighbors = field.get_neighbors(self.x, self.y)

        neighbors_alive = 0
        for cell in neighbors:
            neighbors_alive += cell.val

        if neighbors_alive == 2:
            val = self.val
        elif neighbors_alive == 3:
            val = 1
        else:
            val = 0

        return val


class Field(object):
    def __init__(self, h, w):
        self.h, self.w = h, w
        self.cells = [[None] * w for i in range(h)]

        for i in range(h):
            for j in range(w):
                val = random.randint(0, 1)
                self.cells[i][j] = Cell(i, j, val, self)

    def step(self):
        new_cells = [[None] * self.w for i in range(self.h)]

        for i in range(self.h):
            for j in range(self.w):
                val = self.cells[i][j].get_new_value()
                new_cells[i][j] = Cell(i, j, val, self)

        self.cells = new_cells

    def get_neighbors(self, x, y):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                # sentinel
                if (
                    x + i < 0
                    or y + j < 0
                    or x + i == self.h
                    or y + j == self.w
                    or (i == 0 and j == 0)
                ):
                    continue
                neighbors.append(self.cells[x + i][y + j])

        return neighbors


field = Field(10, 10)

for t in range(100):
    field.step()

