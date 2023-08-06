"""
Window module
Classic Tetris game with play area made out of 10 x 20 square grid
Typical shapes: I, o, L, T, S, Z coded in the model
"""

import pygame
import game.model

# GLOBALS VARS
window_width: int = 1000
window_height: int = 800
play_width: int = 300  # meaning 300 // 10 = 30 width per block
play_height: int = 600  # meaning 600 // 20 = 20 height per block
block_size: int = 30

TOP_LEFT_CORNER_OF_PLAY_AREA_X = (window_width - play_width) // 2
TOP_LEFT_CORNER_OF_PLAY_AREA_Y = window_height - play_height

global GRID


def create_grid(locked_pos=None):
    """Creating an empty game field"""
    if locked_pos is None:
        locked_pos = {}
        # color and size of the play grid build
    grid = [[game.model.black for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                tmp = locked_pos[(j, i)]
                grid[i][j] = tmp
    return grid


def draw_grid(surface, row, col):
    """Drawing lines in play area"""
    start_x = TOP_LEFT_CORNER_OF_PLAY_AREA_X
    start_y = TOP_LEFT_CORNER_OF_PLAY_AREA_Y
    for i in range(row):
        pygame.draw.line(surface, game.model.grey, (start_x, start_y + i * block_size),
                         (start_x + play_width, start_y + i * block_size), 1)  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, game.model.grey, (start_x + j * block_size, start_y),
                             (start_x + j * block_size, start_y + play_height), 1)  # vertical lines


locked_positions: dict = {}  # dictionary of all played pieces
GRID = create_grid(locked_positions)


def draw_window(surface, score):
    """Drawing the game window with text"""
    surface.fill((125, 125, 125))
    # Tetris Title
    font = pygame.font.SysFont('calibri', 60)
    game_title = font.render('TETRIS 1.0', True, game.model.white)

    font2 = pygame.font.SysFont('calibri', 20)
    controls = font2.render('Use arrow keys to control the piece', True, game.model.white)
    controls2 = font2.render('Arrow up rotates, Space instant drops', True, game.model.white)
    current_score = font2.render('Your score: ' + str(score), True, game.model.white)
    surface.blit(game_title, (round(TOP_LEFT_CORNER_OF_PLAY_AREA_X + play_width /
                                    2 - (game_title.get_width() / 2)), 50))
    surface.blit(controls, (round(window_width - (window_width * 0.975)),
                            (round(window_height / 2))))
    surface.blit(controls2, (round(window_width - (window_width * 0.975)),
                             (round(window_height / 2) + 30)))
    surface.blit(current_score, (round(TOP_LEFT_CORNER_OF_PLAY_AREA_X + play_width + 50),
                                 (round(TOP_LEFT_CORNER_OF_PLAY_AREA_Y + play_height / 2) - 300)))

    for i in range(len(GRID)):
        for j in range(len(GRID[i])):
            pygame.draw.rect(surface, GRID[i][j],
                             (TOP_LEFT_CORNER_OF_PLAY_AREA_X + j * block_size,
                              TOP_LEFT_CORNER_OF_PLAY_AREA_Y + i * block_size, block_size,
                              block_size), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (6, 60, 255), (TOP_LEFT_CORNER_OF_PLAY_AREA_X,
                                             TOP_LEFT_CORNER_OF_PLAY_AREA_Y,
                                             play_width, play_height), 5)


def draw_next_shape(shape, surface):
    """Drawing what will be the next shape"""
    font = pygame.font.SysFont('calibri', 30)
    label = font.render('Next Shape', True, game.model.white)

    shape_x = TOP_LEFT_CORNER_OF_PLAY_AREA_X + play_width + 50
    shape_y = TOP_LEFT_CORNER_OF_PLAY_AREA_Y + play_height / 2 - 100
    format_shape = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format_shape):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                pygame.draw.rect(surface, shape.color,
                                 (round(shape_x + j * block_size),
                                  round(shape_y + i * block_size),
                                  block_size, block_size), 0)

    surface.blit(label, (round(shape_x + 10), round(shape_y - 30)))


def draw_text_middle(text, size, color, surface):
    """Function to find the middle of the window"""
    font = pygame.font.SysFont('calibri', size, bold=True)
    label = font.render(text, True, color)

    surface.blit(label,
                 (round(TOP_LEFT_CORNER_OF_PLAY_AREA_X + play_width / 2 - (label.get_width() / 2)),
                  round(TOP_LEFT_CORNER_OF_PLAY_AREA_Y + play_height / 2 - label.get_height() / 2)))
