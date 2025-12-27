import pygame

from gui.Text import Text
from mechanics.clock import clock


class game_over:
    def __init__(
        self,
        screen: pygame.Surface,
        screen_dimensions: tuple,
        script_dir: str,
        message: str,
        tip: str,
    ):
        self.title = Text(screen, fontSize=120)
        self.screen_dimensions = screen_dimensions
        self.description = Text(screen)

        self.background = pygame.image.load(script_dir + "/assets/images/game_over.jpg")
        self.background = pygame.transform.scale(
            self.background, self.screen_dimensions
        )

        self.clock = clock()
        self.message = message
        self.tip = tip

    def update(self, screen: pygame.Surface):
        framerate_clock = pygame.time.Clock()
        running = True
        while running:
            if self.clock.get_seconds() == 10:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False
            screen.blit(self.background, (0, 0))
            self.title.renderText(
                "GAME OVER!",
                "red",
                (
                    self.screen_dimensions[0] / 2,
                    self.screen_dimensions[1] / 2 - self.screen_dimensions[1] * 0.2,
                ),
                True,
            )
            self.description.renderText(
                self.message,
                "white",
                (self.screen_dimensions[0] / 2, self.screen_dimensions[1] / 2),
                True,
            )
            self.description.renderText(
                self.tip,
                "white",
                (
                    self.screen_dimensions[0] / 2,
                    self.screen_dimensions[1] / 2 + self.screen_dimensions[1] * 0.1,
                ),
                True,
            )
            pygame.display.flip()
            framerate_clock.tick(60)
            self.clock.update()
