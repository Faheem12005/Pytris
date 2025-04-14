import random

from settings import FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE, DIRECTIONS, SHAPES, GRID_COLOR, INIT_POS, FIELD_RES
import pygame as pg
from tetromino import Tetromino

class Tetris:
    def __init__(self, app):
        self.app = app
        self.tetromino = Tetromino(random.choice(list(SHAPES.keys())), self)
        self.next_tetromino = Tetromino(random.choice(list(SHAPES.keys())), self)
        self.is_landed = False
        self.grid = [[None for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        self.clear_delay = 100 #in milliseconds, denotes delay to move blocks down
        self.clear_time = 0
        self.lines_to_clear = []

    def draw_next_block(self):
        for block in self.next_tetromino.blocks:
            offseted_block = block.block.move(0.47 * FIELD_RES[0], 0.5 * FIELD_RES[1])
            pg.draw.rect(self.app.screen, pg.Color(block.color), offseted_block)

    def draw_grid(self):
        for x in range(FIELD_WIDTH):
            for y in range(FIELD_HEIGHT):
                block = self.grid[y][x]
                if block is not None:
                    pg.draw.rect(self.app.screen, pg.Color(block.color), block.block)

                rect = pg.Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pg.draw.rect(self.app.screen, GRID_COLOR, rect, width=1)


    def control(self, key):
        if key == pg.K_LEFT:
            self.tetromino.update(DIRECTIONS["LEFT"])
        elif key == pg.K_RIGHT:
            self.tetromino.update(DIRECTIONS["RIGHT"])
        elif key == pg.K_DOWN:
            self.app.fast_anim_trigger = True
        elif key == pg.K_UP:
            self.tetromino.rotate()

    def clear_completed_lines(self):
        for y in range(FIELD_HEIGHT):
            if all(self.grid[y]):
                self.app.score += 100
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

    def is_game_over(self):
        return any(block.pos[0] == INIT_POS[0] and block.pos[1] == INIT_POS[1] for block in self.tetromino.blocks)

    def process_landing(self):
        self.app.fast_anim_trigger = False
        if self.is_game_over():
            self.app.score = 0
            pg.time.wait(300)
            self.__init__(self.app)
            return

        else:
            for block in self.tetromino.blocks:
                self.grid[int(block.pos[1])][int(block.pos[0])] = block
            self.tetromino = self.next_tetromino
            self.next_tetromino = Tetromino(random.choice(list(SHAPES.keys())), self)
            self.is_landed = False

    def update(self):
        #first update game state, then render elements
        if self.app.anim_trigger or self.app.fast_anim_trigger:
            self.tetromino.update(DIRECTIONS["DOWN"])

        if self.is_landed:
            self.process_landing()

        self.clear_completed_lines()
        self.process_cleared_lines()
        self.app.screen.fill("black")
        self.draw_next_block()
        self.tetromino.draw()
        self.draw_grid()





