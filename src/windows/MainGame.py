import pygame
import os
from gui import Text
from utils.stateLoader import stateLoader
from utils.GameState import GameState
from gui.Office import Office

class MainGame:
    def __init__(self, WIDTH: int, HEIGHT: int, script_dir: str):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.loaded_state: dict = {}
        self.script_dir = script_dir;
        self.office = Office((self.WIDTH, self.HEIGHT), self.script_dir)
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
        game_state = GameState.OFFICE_FRONT_LIGHTS
        running: bool = True
        is_office: bool = True
        is_office_front: bool = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   running = False
                   pygame.quit()
                   exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    if game_state is GameState.OFFICE_FRONT_LIGHTS:
                        game_state = GameState.OFFICE_FRONT_DARK
                    if game_state is GameState.OFFICE_FRONT_DARK:
                        game_state = GameState.OFFICE_FRONT_LIGHTS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if game_state is GameState.OFFICE_FRONT_LIGHTS:
                        if self.office.get_back_office_button().mouse_click_handler(event.pos):
                            game_state = GameState.OFFICE_BACK_LIGHTS
                    if game_state is GameState.OFFICE_BACK_LIGHTS:
                        if self.office.get_front_office_button().mouse_click_handler(event.pos):
                            game_state = GameState.OFFICE_FRONT_LIGHTS
                    if game_state is GameState.OFFICE_FRONT_DARK:
                        if self.office.get_back_office_button().mouse_click_handler(event.pos):
                            game_state = GameState.OFFICE_BACK_DARK
                    if game_state is GameState.OFFICE_BACK_DARK:
                        if self.office.get_front_office_button().mouse_click_handler(event.pos):
                            game_state = GameState.OFFICE_FRONT_DARK
            # maybe we should update the image after each press not each frame??
            if game_state is GameState.OFFICE_FRONT_LIGHTS:
                self.office.change_image(self.office.front_office_lights_background)
            if game_state is GameState.OFFICE_BACK_LIGHTS:
                self.office.change_image(self.office.back_office_lights_background)
            self.office.render_office(screen, game_state)
            pygame.display.flip()
