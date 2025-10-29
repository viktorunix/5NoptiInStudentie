import pygame
import os
from gui import Text
from utils.stateLoader import stateLoader

class MainGame:
    def __init__(self, WIDTH: int, HEIGHT: int):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.loaded_state: dict = {}

    def loadingScreen(self, screen: pygame.Surface, clock: pygame.time.Clock):
        loaded = False
        font = pygame.font.Font(None, 74)
        self.loaded_state = stateLoader.loadState()
        while not loaded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loaded = True
            screen.fill((0, 0, 0))
            Text.renderText(screen, font, "Night " + str(self.loaded_state["night"]), pygame.Color("white"),
                (self.WIDTH / 2, self.HEIGHT / 2))
            pygame.display.flip()
            clock.tick(60)
