import pygame as pg
from settings import *

class Block:
    def __init__(self, x, y, tetris, color):
        #x and y are positions in the playing grid
        self.color = color
        self.pos = x + INIT_POS[0], y + INIT_POS[1]
        self.block = pg.Rect(self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.tetris = tetris

    def move(self, direction):
        self.pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
        self.block.move_ip(direction[0] * TILE_SIZE, direction[1] * TILE_SIZE)

    def can_move(self, direction):
        new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
        if new_pos[0] >= FIELD_WIDTH or new_pos[0] < 0 or new_pos[1] >= FIELD_HEIGHT:
            return False
        if self.tetris.grid[int(new_pos[1])][int(new_pos[0])] is not None:
            return False

        return True



class Tetromino:
    def __init__(self, type_block, tetris):
        self.tetris = tetris
        color = self.assign_color(type_block)
        self.blocks = [Block(x, y, tetris, color) for x,y in SHAPES[type_block]]

    @staticmethod
    def assign_color(type_block):
        match type_block:
            case 'I':
                return 'cyan'
            case 'O':
                return 'yellow'
            case 'T':
                return 'purple'
            case 'S':
                return 'green'
            case 'Z':
                return 'red'
            case 'J':
                return 'blue'
            case 'L':
                return 'orange'
            case _:
                return 'white'  # default/fallback


    def move(self, direction):
        for block in self.blocks:
            if not block.can_move(direction):
                if DIRECTIONS["DOWN"] == direction:
                    self.tetris.is_landed = True
                return

        for block in self.blocks:
            block.move(direction)

    def is_collide(self, x, y):
        if x >= FIELD_WIDTH or x < 0 or y >= FIELD_HEIGHT:
            return True
        if self.tetris.grid[y][x] is not None:
            return True

        return False

    def rotate(self):
        new_pos = []
        center_block = self.blocks[0]
        cx, cy = center_block.pos

        for block in self.blocks:
            dx = block.pos[0] - cx
            dy = block.pos[1] - cy

            # Rotate 90 degrees clockwise
            new_x = cx + dy
            new_y = cy - dx

            if self.is_collide(int(new_x), int(new_y)):
                return  # Cancel rotation if collision

            new_pos.append((new_x, new_y))

        for i in range(len(self.blocks)):
            self.blocks[i].pos = new_pos[i]
            self.blocks[i].block = pg.Rect(new_pos[i][0] * TILE_SIZE, new_pos[i][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)


    def draw(self):
        for block in self.blocks:
            pg.draw.rect(self.tetris.app.screen, pg.Color(block.color), block.block)
            pg.draw.rect(self.tetris.app.screen, GRID_COLOR, block.block, width=1)


    def update(self, direction):
        self.move(direction)



