import pygame as pg
from settings import FIELD_RES, FPS, ANIM_TIME_INTERVAL, FAST_ANIM_TIME_INTERVAL
from tetris import Tetris


class App:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode(FIELD_RES)
        self.next_block_text = (pg.font.SysFont('impact', 40)
                                .render("Next Block:", False, pg.Color('white')))
        pg.display.set_caption("tetris")
        self.score_text_heading = (pg.font.SysFont('impact', 40)
                                .render("Score:", False, pg.Color('white')))
        pg.display.set_caption("tetris")
        self.score_text = pg.font.SysFont('impact', 40)
        self.score = 0
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = Tetris(self)

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.fast_anim_trigger = False
        self.anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def check_events(self):
        self.anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

            elif event.type == pg.KEYDOWN:
                self.tetris.control(event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True

    def start(self):
        while True:
            self.check_events()
            self.tetris.update()
            self.screen.blit(self.next_block_text, (0.65 * FIELD_RES[0], 0.35 * FIELD_RES[1]))
            score = self.score_text.render(str(self.score), False, pg.Color('white'))
            self.screen.blit(self.score_text_heading, (0.65 * FIELD_RES[0], 0.15 * FIELD_RES[1]))
            self.screen.blit(score, (0.85 * FIELD_RES[0], 0.15 * FIELD_RES[1]))
            self.clock.tick(FPS)
            pg.display.flip()  # Refresh on-screen display

app = App()
app.start()