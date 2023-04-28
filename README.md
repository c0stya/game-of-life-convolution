# game-of-life-convolution

*Two ways to implement the Game of Life or why I don't like OOP*

I started my career writing Smalltalk programs. It is a language with the purest object-oriented style. Everything is an object and objects communitcate by sending messages. I strongly believed it was a proper way to represent the reality. Later I have changed my mind dramatically. Now I think the proper way of writing code is to keep it minimalistic and practical.

To demonstrate the idea I have written two versions of the Conway's Game of Life in Python. The first one follows the object-oriented style.

## OOP-style version

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

## Convolution-based version

```python
import numpy as np
from scipy.signal import convolve2d

field = np.random.randint(0, 2, size=(10, 10))
kernel = np.ones((3, 3))

for i in range(100):
    new_field = convolve2d(field, kernel, mode="same")
    field = (new_field == 3) + (new_field == 4) * field
```

A few things to explain:

- `convolve2d` with kernel 3x3 of ones is technically a summation within the field 3x3. The result of the summation is placed in the center of the 3x3 field.
- `new_field == 3` indicates that there are 3 cells alive including the central cell. We have two cases:

    * if the central cell was alive then it had 2 neighbors so keep it alive
    * if the central cell was dead then it had 3 neighbors so the central cell would be born the next step

    In either case the central cell should be alive next turn.
- `new_field == 4` indicates there are 4 cells alive including the central cell. We have two cases:

    * if the central cell was alive, then it had 3 neighbors so keep it alive next turn
    * if the central cell was dead, then it had 4 neighbors thus it should be dead next turn

    There is not enough information in the convolved field to distinguish between the two cases above. So we have to look back at the previous state to check if the central cell was alive or not. We do it implicitly by multiplying the convolved field by the previous state of the field.

So, that's it. 9 lines of code to do the same job. The key differences to the previous OOP version:
- we don't really need the cell as a separate class, it is just binary value
- the field is nicely represented by a binary 2D matrix
- the whole logic for the local summation can be represented as convolution operator

Moreover, the second version is more efficient. Convolution uses matrix dot product implicitly which is faster then just summation.

