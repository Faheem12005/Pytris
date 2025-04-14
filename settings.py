import pygame as pg

FPS = 60

TILE_SIZE = 35

FIELD_SIZE = (FIELD_WIDTH, FIELD_HEIGHT) = 10, 20
FIELD_RES = FIELD_WIDTH * TILE_SIZE * 1.7, FIELD_HEIGHT * TILE_SIZE

INIT_POS = FIELD_WIDTH // 2, -1

SHAPES = {
    'L': [(0, 0), (-1, 0), (1, 0), (1, 1)],
    'I': [(0, 0), (-1, 0), (-2, 0), (1, 0)],
    'Z': [(0, 0), (-1, 0), (0, 1), (1, 1)],
    'T': [(0, 0), (-1, 0), (1, 0), (0, 1)],
    'S': [(0, 0), (-1, 1), (0, 1), (1, 0)],
    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'J': [(0, 0), (-1, 0), (1, 0), (-1, 1)],
}

ANIM_TIME_INTERVAL = 400 #milliseconds
FAST_ANIM_TIME_INTERVAL = 15

DIRECTIONS = {
    "DOWN": pg.math.Vector2(0, 1),
    "LEFT": pg.math.Vector2(-1, 0),
    "RIGHT": pg.math.Vector2(1, 0),
}

GRID_COLOR = pg.Color(60, 60, 60)