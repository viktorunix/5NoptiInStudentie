import pygame
import os
from gui import Text
from utils.stateLoader import stateLoader
from gui.Office import Office

class MainGame:
    def __init__(self, WIDTH: int, HEIGHT: int, script_dir: str):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.loaded_state: dict = {}
        self.script_dir = script_dir;
        self.office = Office(self.WIDTH, self.HEIGHT, self.script_dir)
    def loadingScreen(self, screen: pygame.Surface, clock: pygame.time.Clock):
        loaded = False
        font = pygame.font.Font(None, 74)
        self.loaded_state = stateLoader.loadState()
        text = Text.Text(screen, None, 74)
        while not loaded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loaded = True
            screen.fill((0, 0, 0))
            text.renderText("Night " + str(self.loaded_state["night"]), "white", (self.WIDTH / 2, self.HEIGHT / 2/2), True)
            pygame.display.flip()
            clock.tick(60)
        self.main_game(screen)
    def main_game(self,screen: pygame.Surface):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   running = False
            print("am ajuns aici")
            self.office.render_office(screen)
            pygame.display.flip()
