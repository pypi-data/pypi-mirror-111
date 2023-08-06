"""
Model module
Classic Tetris game with play area made out of 10 x 20 square grid
Typical shapes: I, o, L, T, S, Z coded in the model
"""

import random


class Piece:
    """definition of a single shape"""
    rows: int = 20  # y
    columns: int = 10  # x

    def __init__(self, column, row, shape):
        self.x_coordinate = column
        self.y_coordinate = row
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0  # number from 0-3


S = [['.....',
      '.....',
      '..XX.',
      '.XX..',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '...X.',
      '.....']]

Z = [['.....',
      '.....',
      '.XX..',
      '..XX.',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '.X...',
      '.....']]

I = [['..X..',
      '..X..',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      'XXXX.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.XX..',
      '.XX..',
      '.....']]

J = [['.....',
      '.X...',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..XX.',
      '..X..',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '...X.',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '.XX..',
      '.....']]

L = [['.....',
      '...X.',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..X..',
      '..XX.',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '.X...',
      '.....'],
     ['.....',
      '.XX..',
      '..X..',
      '..X..',
      '.....']]

T = [['.....',
      '..X..',
      '.XXX.',
      '.....',
      '.....'],
     ['.....',
      '..X..',
      '..XX.',
      '..X..',
      '.....'],
     ['.....',
      '.....',
      '.XXX.',
      '..X..',
      '.....'],
     ['.....',
      '..X..',
      '.XX..',
      '..X..',
      '.....']]

pink: tuple = (255, 51, 204)
lime: tuple = (0, 204, 0)
orange: tuple = (255, 153, 0)
blue: tuple = (51, 51, 255)
red: tuple = (204, 0, 0)
brown: tuple = (102, 51, 0)
lemon: tuple = (255, 255, 204)
black: tuple = (0, 0, 0)
white: tuple = (255, 255, 255)
grey: tuple = (125, 125, 125)

SHAPES: list = [S, Z, I, O, J, L, T]
SHAPE_COLORS: list = [pink, lime, orange, blue, red, brown, lemon]
# index 0 - 6 represent shape


def get_shape():
    """Func that generates a random shape"""
    global SHAPES, SHAPE_COLORS

    return Piece(5, 0, random.choice(SHAPES))
