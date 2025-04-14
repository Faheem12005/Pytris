import pygame
import pygame as pg
from settings import FIELD_RES, FPS, ANIM_TIME_INTERVAL, FAST_ANIM_TIME_INTERVAL, TILE_SIZE
from tetris import Tetris


class App:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode(FIELD_RES)
        self.next_block_text = (pg.font.Font('Gameplay.ttf', 27)
                                .render("Next Block:", False, pg.Color('white')))
        pg.display.set_caption("tetris")
        self.score_text_heading = (pg.font.Font('Gameplay.ttf', 27)
                                .render("Score:", False, pg.Color('white')))
        pg.display.set_caption("tetris")
        self.score_text = pg.font.Font('Gameplay.ttf', 27)
        self.score = 0
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = Tetris(self)
        self.is_paused = False

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.fast_anim_trigger = False
        self.anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def handle_pause(self):
        if self.is_paused:
            pygame.event.clear()
            self.is_paused = False
        else:
            self.is_paused = True


    def check_events(self):
        self.anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

            elif event.type == pg.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.handle_pause()

                if not self.is_paused:
                    self.tetris.control(event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True

    def draw_side_panel(self):
        self.tetris.draw_next_block()
        self.screen.blit(self.next_block_text, (0.62 * FIELD_RES[0], 0.36 * FIELD_RES[1]))
        score = self.score_text.render(str(self.score), False, pg.Color('white'))
        self.screen.blit(self.score_text_heading, (0.67 * FIELD_RES[0], 0.15 * FIELD_RES[1]))
        self.screen.blit(score, (0.86 * FIELD_RES[0], 0.15 * FIELD_RES[1]))

    def start(self):
        while True:
            self.check_events()
            if self.is_paused:
                self.tetris.draw_grid()  # Optional: draw the game board as-is
                self.tetris.tetromino.draw()
                self.draw_side_panel()
                # Create a transparent overlay
                overlay = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
                overlay.fill((0, 0, 0, 160))
                self.screen.blit(overlay, (0, 0))

                pause_text = pg.font.Font("Gameplay.ttf", 60).render("PAUSED", True, pg.Color("white"))
                self.screen.blit(pause_text, (
                    self.screen.get_width() // 2 - pause_text.get_width() // 2,
                    self.screen.get_height() // 2 - pause_text.get_height() // 2
                ))

            else:
                self.tetris.update()
                self.clock.tick(FPS)
                self.draw_side_panel()

            pg.display.flip()  # Refresh on-screen display

app = App()
app.start()