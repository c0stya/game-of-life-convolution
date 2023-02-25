# game-of-life-convolution

*Two ways to implement the Game of Life or why I don't like OOP*

I started my career writing Smalltalk programs. It is a language with the purest object-oriented style. Everything is an object and objects communitcate by sending messages. I strongly believed it was a proper way to represent the reality. Later I have changed my mind dramatically. Now I think the proper way of writing code is to keep it minimalistic and practical.

To demonstrate the idea I have written two versions of the Conway's Game of Life in Python. The first one follows the object-oriented style.

```python
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
```

The code above is somewhat pathalogical but nicely illustrates the idea. I aggressively follow the object-oriented paradigm and represent classes of the Field and the Cell. The first problem here is that the Cell class is too simplistic. By introducing it we inject redundant methods and complexity. The second problem is that these classes have to keep references to each other. It complicates the logic. As the result we have 70 lines of messy code.

Let's move to the second version.

```python
import numpy as np
from scipy.signal import convolve2d

field = np.random.randint(0, 2, size=(10, 10))
kernel = np.ones((3, 3))

for i in range(100):
    new_field = convolve2d(field, kernel, mode="same")
    field = (new_field == 3) + (new_field == 4) * field
```

So, that's it. 9 lines of code to do the same job. There are few ideas to explain:
- we don't really need the cell as a separate class, it is just binary value
- the field is nicely represented by a binary 2D matrix
- the whole logic for the local summation can be represented as convolution operator

Moreover, the second version is more efficient. Convolution uses matrix dot product implicitly which is faster then just summation.

