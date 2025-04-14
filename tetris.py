import random

from settings import FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE, DIRECTIONS, SHAPES, GRID_COLOR
import pygame as pg
from tetromino import Tetromino

class Tetris:
    def __init__(self, app):
        self.app = app
        self.tetromino = Tetromino(random.choice(list(SHAPES.keys())), self)
        self.is_landed = False
        self.grid = [[None for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.clear_delay = 100 #in milliseconds, denotes delay to move blocks down
        self.clear_time = 0
        self.lines_to_clear = []

    def draw_grid(self):
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                block = self.grid[y][x]
                if block is not None:
                    pg.draw.rect(self.app.screen, "cyan", block.block)

                rect = pg.Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pg.draw.rect(self.app.screen, GRID_COLOR, rect, width=1)


    def control(self, key):
        if key == pg.K_LEFT:
            self.tetromino.update(DIRECTIONS["LEFT"])
        elif key == pg.K_RIGHT:
            self.tetromino.update(DIRECTIONS["RIGHT"])
        elif key == pg.K_DOWN:
            self.tetromino.update(DIRECTIONS["DOWN"])
        elif key == pg.K_UP:
            self.tetromino.rotate()

    def clear_completed_lines(self):
        for y in range(FIELD_HEIGHT):
            if all(self.grid[y]):
                self.grid[y] = [None for _ in range(FIELD_WIDTH)]
                if not self.lines_to_clear:
                    self.clear_time = pg.time.get_ticks()
                self.lines_to_clear.append(y)


    def process_cleared_lines(self):
        if pg.time.get_ticks() - self.clear_time >= self.clear_delay:
            for y in self.lines_to_clear:
                for row in range(y, 0, -1):
                    for x in range(FIELD_WIDTH):
                        block_above = self.grid[row - 1][x]  # get the block above
                        self.grid[row][x] = block_above  # assign it to current row
                        self.grid[row - 1][x] = None
                        if self.grid[row][x] is not None:
                            block_above.move(DIRECTIONS["DOWN"])

                self.grid[0] = [None for _ in range(FIELD_WIDTH)]
            self.lines_to_clear = []
            self.clear_time = 0

            #check again to see if cascading full lines are formed
            self.clear_completed_lines()


    def update(self):
        #first update game state, then render elements
        if self.app.anim_trigger:
            self.tetromino.update(DIRECTIONS["DOWN"])

        #game loop for spawning new tetrominos :P
        if self.is_landed:
            self.tetromino = self.tetromino = Tetromino(random.choice(list(SHAPES.keys())), self)
            self.is_landed = False

        self.clear_completed_lines()
        self.process_cleared_lines()
        self.app.screen.fill("black")
        self.tetromino.draw()
        self.draw_grid()





