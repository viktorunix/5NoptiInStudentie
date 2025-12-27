import os
from asyncio.unix_events import FastChildWatcher

import pygame

from gui import Text
from gui.Camera import Camera
from gui.Office import Office
from mechanics.BigBug import BigBug
from mechanics.clock import clock
from mechanics.OxygenMeter import OxygenMeter
from mechanics.spray import spray
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

        self.last_camera_state = None
        self.last_office_state = None

        self.bug_enemy = BigBug("BigBug", camera_state.BATHROOM_HALLWAY, 10, script_dir)
        self.spray = spray(script_dir)

        self.oxygen = OxygenMeter(max_oxygen=100, regen_rate=0.05)
        self.game_over = False

        self.office_image_map = {
            office_state.OFFICE_FRONT_LIGHTS: self.office.front_office_lights_background,
            office_state.OFFICE_BACK_LIGHTS: self.office.back_office_lights_background,
            office_state.OFFICE_FRONT_LIGHTS_OPEN: self.office.front_office_lights_open_background,
            office_state.OFFICE_BACK_LIGHTS_OPEN: self.office.back_office_lights_open_background,
            # office_state.OFFICE_FRONT_DARK: self.office.front_office_dark_background,
            # office_state.OFFICE_BACK_DARK: self.office_back_office_dark_background
        }

        self.camera_image_map = {
            camera_state.BATHROOM_HALLWAY: self.camera.bath_hallway_background,
            camera_state.MAIN_HALLWAY_A: self.camera.main_hallway_a_background,
            camera_state.MAIN_HALLWAY_OFFICE: self.camera.main_hallway_office_background,
            camera_state.MAIN_HALLWAY_B: self.camera.main_hallway_b_background,
            camera_state.STAIRWAY: self.camera.staircase_background,
            camera_state.BATHROOM_HALLWAY_BUG: self.camera.bath_hallway_bug_background,
            camera_state.MAIN_HALLWAY_A_BUG: self.camera.main_hallway_a_bug_background,
            camera_state.MAIN_HALLWAY_OFFICE_BUG: self.camera.main_hallway_office_bug_background,
            camera_state.MAIN_HALLWAY_B_BUG: self.camera.main_hallway_b_bug_background,
            camera_state.STAIRWAY_BUG: self.camera.staircase_bug_background,
        }
        """this is used for updating the camera if the bug dissapears from screen"""
        self.bug_view_map = {
            camera_state.BATHROOM_HALLWAY_BUG: camera_state.BATHROOM_HALLWAY,
            camera_state.MAIN_HALLWAY_A_BUG: camera_state.MAIN_HALLWAY_A,
            camera_state.MAIN_HALLWAY_B_BUG: camera_state.MAIN_HALLWAY_B,
            camera_state.MAIN_HALLWAY_OFFICE_BUG: camera_state.MAIN_HALLWAY_OFFICE,
            camera_state.STAIRWAY_BUG: camera_state.STAIRWAY,
        }
        self.cam_glitch_sound = pygame.mixer.Sound(
            script_dir + "/assets/audio/cam_glitch.mp3"
        )
        self.window_open_sound = pygame.mixer.Sound(
            script_dir + "/assets/audio/window_open.mp3"
        )
        self.window_close_sound = pygame.mixer.Sound(
            script_dir + "/assets/audio/window_close.mp3"
        )
        self.door_open_sound = pygame.mixer.Sound(
            script_dir + "/assets/audio/door_open.mp3"
        )
        self.door_close_sound = pygame.mixer.Sound(
            script_dir + "/assets/audio/door_close.mp3"
        )

    def loadingScreen(
        self, screen: pygame.Surface, clock: pygame.time.Clock, new_game: bool = False
    ):
        loaded = False
        # font = pygame.font.Font(None, self.HEIGHT // 10)
        if not new_game:
            self.loaded_state = stateLoader.load_state()
        else:
            self.loaded_state = stateLoader.new_state()
        text = Text.Text(screen, None, self.HEIGHT // 10)
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
                (self.WIDTH / 2, self.HEIGHT / 3),
                True,
            )
            pygame.display.flip()
            clock.tick(60)
            self.ticks += 1
        self.main_game(screen)

    def camera_event_handler(self, event):
        if self.camera.get_office_button().mouse_click_handler(event.pos):
            self.__camera_state = camera_state.NONE
            return

        cam_buttons = [
            (
                self.camera.get_main_hallway_b_button(),
                camera_state.MAIN_HALLWAY_B,
                camera_state.MAIN_HALLWAY_B_BUG,
            ),
            (
                self.camera.get_main_hallway_a_button(),
                camera_state.MAIN_HALLWAY_A,
                camera_state.MAIN_HALLWAY_A_BUG,
            ),
            (
                self.camera.get_main_hallway_office_button(),
                camera_state.MAIN_HALLWAY_OFFICE,
                camera_state.MAIN_HALLWAY_OFFICE_BUG,
            ),
            (
                self.camera.get_staircase_button(),
                camera_state.STAIRWAY,
                camera_state.STAIRWAY_BUG,
            ),
            (
                self.camera.get_bath_hallway_button(),
                camera_state.BATHROOM_HALLWAY,
                camera_state.BATHROOM_HALLWAY_BUG,
            ),
        ]
        current_bug_loc = self.bug_enemy.get_location()
        for button, normal_state, bug_state in cam_buttons:
            if button.mouse_click_handler(event.pos):
                if current_bug_loc == normal_state:
                    self.__camera_state = bug_state
                else:
                    self.__camera_state = normal_state
                return

    def new_office_event_handler(self, event):
        max_scroll_x = self.office.office.get_width() - self.WIDTH
        current_x = self.office.camera_x

        is_front = self.__office_state in [
            office_state.OFFICE_FRONT_LIGHTS,
            office_state.OFFICE_FRONT_LIGHTS_OPEN,
        ]
        is_back = self.__office_state in [
            office_state.OFFICE_BACK_LIGHTS,
            office_state.OFFICE_BACK_LIGHTS_OPEN,
        ]
        if is_front:
            # opening camera
            if current_x <= 30:
                if self.office.get_camera_button().mouse_click_handler(event.pos):
                    if self.bug_enemy.get_location() is camera_state.MAIN_HALLWAY_A:
                        self.__camera_state = camera_state.MAIN_HALLWAY_A_BUG
                    else:
                        self.__camera_state = camera_state.MAIN_HALLWAY_A

            # turning around
            if current_x >= max_scroll_x:
                if self.office.get_back_office_button().mouse_click_handler(event.pos):
                    self.office.camera_x = 0
                    if not self.__window_open:
                        self.__office_state = office_state.OFFICE_BACK_LIGHTS
                    else:
                        self.__office_state = office_state.OFFICE_BACK_LIGHTS_OPEN

            # toggle door
            if self.office.get_door_button().mouse_click_handler(
                event.pos, scroll_x=current_x
            ):
                print("daaaa")
                if not self.__door_open:
                    self.door_open_sound.play()
                    self.__office_state = office_state.OFFICE_FRONT_LIGHTS_OPEN
                    self.__door_open = True
                else:
                    self.door_close_sound.play()
                    self.__office_state = office_state.OFFICE_FRONT_LIGHTS
                    self.__door_open = False
        if is_back:
            if current_x == 0:
                if self.office.get_front_office_button().mouse_click_handler(event.pos):
                    self.office.camera_x = (
                        self.office.front_office_lights_background.get_image().get_width()
                        - self.WIDTH
                    )
                    if not self.__door_open:
                        self.__office_state = office_state.OFFICE_FRONT_LIGHTS
                    else:
                        self.__office_state = office_state.OFFICE_FRONT_LIGHTS_OPEN
            if current_x >= max_scroll_x:
                if self.office.get_window_button().mouse_click_handler(event.pos):
                    if not self.__window_open:
                        self.window_open_sound.play()
                        self.__office_state = office_state.OFFICE_BACK_LIGHTS_OPEN
                        self.__window_open = True
                    else:
                        self.window_close_sound.play()
                        self.__office_state = office_state.OFFICE_BACK_LIGHTS
                        self.__window_open = False

    def new_update_image(self, screen):
        if self.__camera_state is not camera_state.NONE:
            if self.__camera_state is not self.last_camera_state:
                target_img = self.camera_image_map.get(self.__camera_state)
                if target_img:
                    self.camera.change_image(target_img)
                self.last_camera_state = self.__camera_state
            self.camera.render_camera(screen, self.__camera_state)

        else:
            if self.__office_state is not self.last_office_state:
                target_img = self.office_image_map.get(self.__office_state)
                if target_img:
                    self.office.change_image(target_img)
                self.last_office_state = self.__office_state
            self.office.render_office(screen, self.__office_state)

    def update_bug_camera(self):
        """if the player is on the cam where the bug is but meanwhile the bug moves the player still sees it so this is why i wrote this function"""

        if self.__camera_state in self.bug_view_map:
            required_location = self.bug_view_map[self.__camera_state]
            if self.bug_enemy.get_location() is not required_location:
                self.cam_glitch_sound.play()
                self.__camera_state = required_location

    def handle_spray_mechanic(self):
        if self.game_over:
            return
        if self.__camera_state is not camera_state.NONE:
            return
        if self.__office_state in [
            office_state.OFFICE_FRONT_LIGHTS_OPEN,
            office_state.OFFICE_FRONT_DARK_OPEN,
        ]:
            print("aici")
            if self.spray.use_spray():
                toxicity = self.spray.get_toxicity()
                is_suffocating = self.oxygen.deplete(toxicity)
                if is_suffocating:
                    print("GAME OVER: TE-AI SUFOCAT")
                    self.game_over = True
                if self.bug_enemy.get_location() is camera_state.MAIN_HALLWAY_OFFICE:
                    self.bug_enemy.force_retreat(camera_state.BATHROOM_HALLWAY)

    def main_game(self, screen: pygame.Surface):
        """main gameloop"""
        clock_text = Text.Text(screen)
        framerate_clock = pygame.time.Clock()
        ammo_text = Text.Text(screen, fontSize=30)
        pygame.mixer.music.load(self.script_dir + "/assets/audio/office_background.mp3")
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(loops=-1, start=0.0)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    # just testing this will be removed
                    print("z was pressed")
                    if self.__office_state is office_state.OFFICE_FRONT_LIGHTS:
                        self.__office_state = office_state.OFFICE_FRONT_DARK
                    elif self.__office_state is office_state.OFFICE_FRONT_DARK:
                        self.__office_state = office_state.OFFICE_FRONT_LIGHTS
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.__camera_state is not camera_state.NONE:
                        self.camera_event_handler(event)
                    else:
                        self.new_office_event_handler(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.handle_spray_mechanic()

            self.new_update_image(screen)
            self.bug_enemy.update()
            self.spray.update()
            self.update_bug_camera()
            if self.__window_open:
                self.oxygen.update()

            if self.__camera_state is camera_state.NONE:
                clock_text.renderText(
                    self.__clock.get_hour_text() + " AM",
                    "white",
                    (self.WIDTH - 100, 40),
                    True,
                )
                ammo_text.renderText("Oxygen Meter:", "white", (20, self.HEIGHT - 70))
                self.oxygen.render_bar(screen, 10, self.HEIGHT - 40)
                ammo_count = self.spray.current_uses
                color = "white" if ammo_count > 0 else "red"
                ammo_text.renderText(
                    f"Spray: {ammo_count}", color, (20, self.HEIGHT - 100)
                )
            pygame.display.flip()
            framerate_clock.tick(60)
            self.__clock.update()
