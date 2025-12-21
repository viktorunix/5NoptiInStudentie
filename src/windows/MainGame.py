import os
from asyncio.unix_events import FastChildWatcher

import pygame

from gui import Text
from gui.Camera import Camera
from gui.Office import Office
from mechanics.clock import clock
from utils.camera_state import camera_state
from utils.office_state import office_state
from utils.stateLoader import stateLoader


class MainGame:
    def __init__(self, WIDTH: int, HEIGHT: int, script_dir: str):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.loaded_state: dict = {}
        self.script_dir = script_dir
        self.office = Office((self.WIDTH, self.HEIGHT), self.script_dir)
        self.camera = Camera((self.WIDTH, self.HEIGHT), self.script_dir)
        self.ticks = 0
        self.__camera_state: camera_state = camera_state.NONE
        self.__office_state = office_state.OFFICE_FRONT_LIGHTS
        self.__clock = clock()
        self.__door_open: bool = False
        self.__window_open: bool = False
        self.__lights_on: bool = True

    def loadingScreen(
        self, screen: pygame.Surface, clock: pygame.time.Clock, new_game: bool = False
    ):
        loaded = False
        font = pygame.font.Font(None, 74)
        if not new_game:
            self.loaded_state = stateLoader.load_state()
        else:
            self.loaded_state = stateLoader.new_state()
        text = Text.Text(screen, None, 74)
        while not loaded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if self.ticks == 60 * 3:
                loaded = True
            screen.fill((0, 0, 0))
            text.renderText(
                "Night " + str(self.loaded_state["night"]),
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 / 2),
                True,
            )
            pygame.display.flip()
            clock.tick(60)
            self.ticks += 1
        self.main_game(screen)

    def camera_event_handler_3(self, event):
        if self.camera.get_office_button().mouse_click_handler(event.pos):
            self.__camera_state = camera_state.NONE
        elif self.camera.get_main_hallway_b_button().mouse_click_handler(event.pos):
            self.__camera_state = camera_state.MAIN_HALLWAY_B
        elif self.camera.get_main_hallway_a_button().mouse_click_handler(event.pos):
            self.__camera_state = camera_state.MAIN_HALLWAY_A
        elif self.camera.get_staircase_button().mouse_click_handler(event.pos):
            self.__camera_state = camera_state.STAIRWAY
        elif self.camera.get_bath_hallway_button().mouse_click_handler(event.pos):
            self.__camera_state = camera_state.BATHROOM_HALLWAY
        elif self.camera.get_main_hallway_office_button().mouse_click_handler(
            event.pos
        ):
            self.__camera_state = camera_state.MAIN_HALLWAY_OFFICE

    def office_event_handler(self, event):
        """Handling events in regards with office_state"""
        if (
            self.__office_state is office_state.OFFICE_FRONT_LIGHTS
            or self.__office_state is office_state.OFFICE_FRONT_LIGHTS_OPEN
        ):
            if self.office.get_camera_button().mouse_click_handler(event.pos):
                self.__camera_state = camera_state.MAIN_HALLWAY_A
            if self.office.get_back_office_button().mouse_click_handler(event.pos):
                self.__office_state = office_state.OFFICE_BACK_LIGHTS
            if self.office.get_door_button().mouse_click_handler(event.pos):
                print(str(self.__door_open))
                if not self.__door_open:
                    self.__office_state = office_state.OFFICE_FRONT_LIGHTS_OPEN
                    self.__door_open = True
                else:
                    print("a ajuns aici")
                    self.__office_state = office_state.OFFICE_FRONT_LIGHTS
                    self.__door_open = False
        # if self.__office_state is office_state.OFFICE_FRONT_LIGHTS:

        if self.__office_state is office_state.OFFICE_BACK_LIGHTS:
            if self.office.get_front_office_button().mouse_click_handler(event.pos):
                if not self.__door_open:
                    self.__office_state = office_state.OFFICE_FRONT_LIGHTS
                else:
                    self.__office_state = office_state.OFFICE_FRONT_LIGHTS_OPEN
        elif self.__office_state is office_state.OFFICE_FRONT_DARK:
            if self.office.get_back_office_button().mouse_click_handler(event.pos):
                self.__office_state = office_state.OFFICE_BACK_DARK
        elif self.__office_state is office_state.OFFICE_BACK_DARK:
            if self.office.get_front_office_button().mouse_click_handler(event.pos):
                self.__office_state = office_state.OFFICE_FRONT_DARK

    def update_image(self, screen):
        """Updates the screen image background depending on each state"""
        # maybe we should update the image after each press not each frame??
        print(str(self.__office_state))
        if self.__office_state is office_state.OFFICE_FRONT_LIGHTS:
            self.office.change_image(self.office.front_office_lights_background)
        if self.__office_state is office_state.OFFICE_BACK_LIGHTS:
            self.office.change_image(self.office.back_office_lights_background)

        if self.__office_state is office_state.OFFICE_FRONT_LIGHTS_OPEN:
            self.office.change_image(self.office.front_office_lights_open_background)
        if self.__camera_state is camera_state.NONE:
            self.office.render_office(screen, self.__office_state)
        else:
            self.camera.render_camera(screen, self.__camera_state)
        if self.__camera_state is camera_state.STAIRWAY:
            self.camera.change_image(self.camera.staircase_background)
        if self.__camera_state is camera_state.MAIN_HALLWAY_A:
            self.camera.change_image(self.camera.main_hallway_a_background)
        if self.__camera_state is camera_state.MAIN_HALLWAY_B:
            self.camera.change_image(self.camera.main_hallway_b_background)
        if self.__camera_state is camera_state.BATHROOM_HALLWAY:
            self.camera.change_image(self.camera.bath_hallway_background)
        if self.__camera_state is camera_state.MAIN_HALLWAY_OFFICE:
            self.camera.change_image(self.camera.main_hallway_office_background)

    def main_game(self, screen: pygame.Surface):
        """main gameloop"""
        clock_text = Text.Text(screen)
        framerate_clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    # just testing this will be removed
                    print("z was pressed")
                    if self.__office_state is office_state.OFFICE_FRONT_LIGHTS:
                        self.__office_state = office_state.OFFICE_FRONT_DARK
                    elif self.__office_state is office_state.OFFICE_FRONT_DARK:
                        self.__office_state = office_state.OFFICE_FRONT_LIGHTS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.__camera_state is not camera_state.NONE:
                        self.camera_event_handler_3(event)
                    else:
                        self.office_event_handler(event)

            self.update_image(screen)
            clock_text.renderText(
                "0"
                + str(self.__clock.get_minutes())
                + ":"
                + str(self.__clock.get_seconds())
                + " AM",
                "white",
                (self.WIDTH - 100, 40),
                True,
            )
            pygame.display.flip()
            framerate_clock.tick(60)
            self.__clock.update()
