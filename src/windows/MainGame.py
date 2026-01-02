import pygame
from cv2 import DISOPTICAL_FLOW_PRESET_ULTRAFAST

from gui import Text
from gui.Camera import Camera
from gui.Office import Office
from mechanics.BigBug import BigBug
from mechanics.Clock import Clock
from mechanics.OxygenMeter import OxygenMeter
from mechanics.SmallBugs import SmallBugs
from mechanics.Spray import Spray
from utils.Difficulty import Difficulty
from utils.game_state import camera_state, office_state
from utils.stateLoader import get_resource_path, stateLoader
from windows.GameOver import GameOver
from windows.JumpscareAnimation import JumpscareAnimation
from windows.NightPass import NightPass


class MainGame:
    def __init__(self, WIDTH: int, HEIGHT: int, video_background=None):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.loaded_state: dict = {}
        self.video_background = video_background
        self.office = Office((self.WIDTH, self.HEIGHT))
        self.camera = Camera((self.WIDTH, self.HEIGHT), self.video_background)
        self.ticks = 0
        self.camera_state: camera_state = camera_state.NONE
        self.office_state = office_state.OFFICE_FRONT
        self.clock = Clock()
        self.door_open: bool = False
        self.window_open: bool = False
        self.lights_on: bool = True
        self.is_restocking: bool = False
        self.cam_glitch_alpha = 70
        self.cam_glitch_channel = pygame.mixer.Channel(0)
        self.cam_glitch_message = ""
        self.last_camera_state = None
        self.last_office_state = None

        self.bug_enemy = BigBug("BigBug", camera_state.BATHROOM_HALLWAY, 10)
        self.spray = Spray()
        self.small_bugs = SmallBugs(30, 5)

        self.oxygen = OxygenMeter(100, 0.05, self.HEIGHT)
        self.game_over = False

        self.office_image_map = {
            office_state.OFFICE_FRONT: self.office.office_front_background,
            office_state.OFFICE_BACK: self.office.office_back_background,
            office_state.OFFICE_FRONT_OPEN: self.office.office_front_open_background,
            office_state.OFFICE_BACK_OPEN: self.office.office_back_open_background,
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
            get_resource_path("/assets/audio/cam_glitch.mp3")
        )
        self.window_open_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/window_open.mp3")
        )
        self.window_close_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/window_close.mp3")
        )
        self.door_open_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/door_open.mp3")
        )
        self.door_close_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/door_close.mp3")
        )
        self.jumpscare_animation = JumpscareAnimation(self.HEIGHT, self.WIDTH)

    def loadingScreen(
        self, screen: pygame.Surface, clock: pygame.time.Clock, new_game: bool = False
    ):
        loaded = False
        # font = pygame.font.Font(None, self.HEIGHT // 10)
        if not new_game:
            self.loaded_state = stateLoader.load_state()
        else:
            self.loaded_state = stateLoader.new_state()

        while not loaded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if self.ticks == 60 * 10:
                loaded = True
            screen.fill((0, 0, 0))
            text = Text.Text(screen, fontSize=100)
            text.renderText(
                "Night " + str(self.loaded_state["night"]),
                "white",
                (self.WIDTH / 2, self.HEIGHT / 3),
                True,
            )

            text = Text.Text(screen)
            text.renderText(
                "Dont let bugs in your room, especially the big one",
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 + text.getSize()),
                True,
            )
            text.renderText(
                "Open the door and use the spray to repell the big bug",
                "white",
                (
                    self.WIDTH / 2,
                    self.HEIGHT / 2 + 2 * text.getSize(),
                ),
                True,
            )
            text.renderText(
                "Dont leave the window or the door open for too long or you risk an infestation",
                "white",
                (
                    self.WIDTH / 2,
                    self.HEIGHT / 2 + 3 * text.getSize(),
                ),
                True,
            )
            text.renderText(
                "Using too much spray would suffocate you, make sure you ventilate the room",
                "white",
                (
                    self.WIDTH / 2,
                    self.HEIGHT / 2 + 4 * text.getSize(),
                ),
                True,
            )
            pygame.display.flip()
            clock.tick(60)
            self.ticks += 1
        df = Difficulty()
        self.bug_enemy.ai_level = df.bug_ai[int(self.loaded_state["night"]) - 1]
        self.spray.max_uses = df.spray_uses[int(self.loaded_state["night"]) - 1]
        self.spray.current_uses = self.spray.max_uses
        self.small_bugs.move_interval = df.spray_uses[
            int(self.loaded_state["night"]) - 1
        ]
        self.main_game(screen)

    def camera_event_handler(self, event):
        if self.camera.office_button.mouse_click_handler(event.pos):
            self.camera_state = camera_state.NONE
            return

        cam_buttons = [
            (
                self.camera.main_hallway_b_button,
                camera_state.MAIN_HALLWAY_B,
                camera_state.MAIN_HALLWAY_B_BUG,
            ),
            (
                self.camera.main_hallway_a_button,
                camera_state.MAIN_HALLWAY_A,
                camera_state.MAIN_HALLWAY_A_BUG,
            ),
            (
                self.camera.main_hallway_office_button,
                camera_state.MAIN_HALLWAY_OFFICE,
                camera_state.MAIN_HALLWAY_OFFICE_BUG,
            ),
            (
                self.camera.staircase_button,
                camera_state.STAIRWAY,
                camera_state.STAIRWAY_BUG,
            ),
            (
                self.camera.bath_hallway_button,
                camera_state.BATHROOM_HALLWAY,
                camera_state.BATHROOM_HALLWAY_BUG,
            ),
        ]
        if (
            self.camera_state in [camera_state.STAIRWAY_BUG, camera_state.STAIRWAY]
            and not self.is_restocking
        ):
            if self.camera.restock_spray_button.mouse_click_handler(event.pos):
                self.is_restocking = True
        current_bug_loc = self.bug_enemy.get_location()
        for button, normal_state, bug_state in cam_buttons:
            if button.mouse_click_handler(event.pos):
                if current_bug_loc == normal_state:
                    self.camera_state = bug_state
                else:
                    self.camera_state = normal_state
                return

    def new_office_event_handler(self, event):
        max_scroll_x = self.office.office.get_width() - self.WIDTH
        current_x = self.office.camera_x

        is_front = self.office_state in [
            office_state.OFFICE_FRONT,
            office_state.OFFICE_FRONT_OPEN,
        ]
        is_back = self.office_state in [
            office_state.OFFICE_BACK,
            office_state.OFFICE_BACK_OPEN,
        ]
        if is_front:
            # opening camera
            if current_x <= 30:
                if self.office.camera_button.mouse_click_handler(event.pos):
                    if self.bug_enemy.get_location() is camera_state.MAIN_HALLWAY_A:
                        self.camera_state = camera_state.MAIN_HALLWAY_A_BUG
                    else:
                        self.camera_state = camera_state.MAIN_HALLWAY_A

            # turning around
            if current_x >= max_scroll_x:
                if self.office.back_office_button.mouse_click_handler(event.pos):
                    self.office.camera_x = 0
                    if not self.window_open:
                        self.office_state = office_state.OFFICE_BACK
                    else:
                        self.office_state = office_state.OFFICE_BACK_OPEN

            # toggle door
            if self.office.door_button.mouse_click_handler(
                event.pos, scroll_x=current_x
            ):
                print("daaaa")
                if not self.door_open:
                    self.door_open_sound.play()
                    self.office_state = office_state.OFFICE_FRONT_OPEN
                    self.door_open = True
                else:
                    self.door_close_sound.play()
                    self.office_state = office_state.OFFICE_FRONT
                    self.door_open = False
            if self.office.spray_button.mouse_click_handler(
                event.pos, scroll_x=current_x
            ):
                self.handle_spray_mechanic()
        if is_back:
            if current_x == 0:
                if self.office.front_office_button.mouse_click_handler(event.pos):
                    self.office.camera_x = (
                        self.office.office_front_background.get_image().get_width()
                        - self.WIDTH
                    )
                    if not self.door_open:
                        self.office_state = office_state.OFFICE_FRONT
                    else:
                        self.office_state = office_state.OFFICE_FRONT_OPEN
            if current_x >= max_scroll_x:
                if self.office.window_button.mouse_click_handler(event.pos):
                    if not self.window_open:
                        self.office.window_button.set_text("Close")
                        self.window_open_sound.play()
                        self.office_state = office_state.OFFICE_BACK_OPEN
                        self.window_open = True
                    else:
                        self.office.window_button.set_text("Open")
                        self.window_close_sound.play()
                        self.office_state = office_state.OFFICE_BACK
                        self.window_open = False

    def new_update_image(self, screen):
        if self.camera_state is not camera_state.NONE:
            if self.camera_state is not self.last_camera_state:
                target_img = self.camera_image_map.get(self.camera_state)
                if target_img:
                    self.camera.change_image(target_img)
                self.last_camera_state = self.camera_state
            self.camera.render_camera(screen, self.camera_state, self.cam_glitch_alpha)

        else:
            if self.office_state is not self.last_office_state:
                target_img = self.office_image_map.get(self.office_state)
                if target_img:
                    self.office.change_image(target_img)
                self.last_office_state = self.office_state
            self.office.render_office(screen, self.office_state)

    def update_bug_camera(self, screen):
        """if the player is on the cam where the bug is but meanwhile the bug moves the player still sees it so this is why i wrote this function"""

        if not self.cam_glitch_channel.get_busy():
            self.cam_glitch_alpha = 70
            self.cam_glitch_message = ""
        if self.camera_state is not camera_state.NONE:
            glitch_message = Text.Text(screen)
            glitch_message.renderText(
                self.cam_glitch_message,
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 - self.HEIGHT * 0.2),
                True,
            )
        if self.camera_state in self.bug_view_map:
            required_location = self.bug_view_map[self.camera_state]
            if self.bug_enemy.get_location() is not required_location:
                self.cam_glitch_channel = self.cam_glitch_sound.play()
                self.cam_glitch_alpha = 250
                self.cam_glitch_message = "Camera indisponibila"
                self.camera_state = required_location

        # make bug appear on camera if the bug is on that location
        if self.camera_state is self.bug_enemy.get_location():
            self.cam_glitch_channel = self.cam_glitch_sound.play()
            self.cam_glitch_alpha = 250
            self.cam_glitch_message = "Camera indisponibila"

            # we get every key in the dictionary and put it in a list
            states = [
                key
                for key, val in self.bug_view_map.items()
                if val is self.camera_state
            ]
            if states:
                self.camera_state = states[0]

    def check_game_over(self, screen: pygame.Surface) -> bool:
        if self.bug_enemy.jumpscare:
            pygame.mixer.music.stop()
            self.jumpscare_animation.play(screen)
            if self.spray.current_uses != 0:
                gm = GameOver(
                    screen,
                    (self.WIDTH, self.HEIGHT),
                    "If the big bug is near your door",
                    "open the door and use the spray to repell it",
                )
                gm.update(screen)
            else:
                gm = GameOver(
                    screen,
                    (self.WIDTH, self.HEIGHT),
                    "The spray can has limited uses",
                    "it should be use in critical moments and restocked when needed",
                )
                gm.update(screen)
            return True
        if self.oxygen.current_oxygen <= 0:
            self.jumpscare_animation.play(screen)
            pygame.mixer.music.stop()
            gm = GameOver(
                screen,
                (self.WIDTH, self.HEIGHT),
                "You suffocated from using too much spray",
                "open the window to restore the oxygen level ",
            )
            gm.update(screen)
            return True
        if self.small_bugs.check_limit():
            self.jumpscare_animation.play(screen)
            pygame.mixer.music.stop()
            gm = GameOver(
                screen,
                (self.WIDTH, self.HEIGHT),
                "Too many bugs entered your room",
                "don't leave open doors or windows next time",
            )
            gm.update(screen)
            return True
        return False

    def check_night_passed(self, screen: pygame.Surface) -> bool:
        if self.clock.get_minutes() == 6:
            pygame.mixer.music.stop()
            stateLoader.advance_night(self.loaded_state)
            np = NightPass(screen, (self.WIDTH, self.HEIGHT))
            np.update(screen)
            return True
        return False

    def handle_spray_mechanic(self):
        if self.game_over:
            return
        if self.camera_state is not camera_state.NONE:
            return
        if self.office_state is office_state.OFFICE_FRONT_OPEN:
            print("aici")
            if self.spray.use_spray():
                toxicity = self.spray.get_toxicity()
                is_suffocating = self.oxygen.deplete(toxicity)
                if is_suffocating:
                    print("GAME OVER: TE-AI SUFOCAT")
                    self.game_over = True
                if self.bug_enemy.get_location() is camera_state.MAIN_HALLWAY_OFFICE:
                    self.bug_enemy.force_retreat(camera_state.BATHROOM_HALLWAY)
        else:
            if self.spray.use_spray():
                toxicity = self.spray.get_toxicity()
                is_suffocating = self.oxygen.deplete(toxicity)
                if is_suffocating:
                    self.game_over = True
                self.small_bugs.decrease_counter()

    def update_office_resources(self, screen):
        """Renders clock, oxygen meter number of sprays and bugs on screen"""

        # clock
        if self.camera_state is camera_state.NONE:
            clock_text = Text.Text(screen)
            clock_text.renderText(
                self.clock.get_hour_text() + " AM",
                "white",
                (self.WIDTH * 19 / 20, self.HEIGHT * 1 / 20),
                True,
            )

            # small bugs meter
            small_bugs_text = Text.Text(screen, fontSize=50)
            small_bugs_text.renderText(
                "Bugs in room "
                + str(self.small_bugs.current_bugs)
                + "/"
                + str(self.small_bugs.limit),
                "white",
                (self.WIDTH * 1 / 40, self.HEIGHT * 34 / 40),
            )

            # Oxygen meter
            oxygen_meter_text = Text.Text(screen, fontSize=60)
            oxygen_meter_text.renderText(
                "Oxygen Meter:", "white", (self.WIDTH * 1 / 40, self.HEIGHT * 36 / 40)
            )
            self.oxygen.render_bar(screen, self.WIDTH * 1 / 40, self.HEIGHT * 37.2 / 40)

            # Spray uses
            spray_uses_text = Text.Text(screen, fontSize=50)
            spray_count = self.spray.current_uses
            color = "white" if spray_count > 0 else "red"
            spray_uses_text.renderText(
                "Spray: " + str(spray_count),
                color,
                (self.WIDTH * 1 / 40, self.HEIGHT * 35 / 40),
            )
        if self.is_restocking:
            self.camera.restock_spray_button.set_text(
                f"Restocking in {int((self.spray.restock_max - self.spray.restock_timer) / 60)}"
            )
            self.is_restocking = self.spray.restock()
        else:
            self.camera.restock_spray_button.set_text("Restock")

    def main_game(self, screen: pygame.Surface):
        """main gameloop"""
        framerate_clock = pygame.time.Clock()
        pygame.mixer.music.load(
            get_resource_path("/assets/audio/office_background.mp3")
        )
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(loops=-1, start=0.0)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.camera_state is not camera_state.NONE:
                        self.camera_event_handler(event)
                    else:
                        self.new_office_event_handler(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.handle_spray_mechanic()

            if self.check_game_over(screen):
                break
            if self.check_night_passed(screen):
                break
            self.new_update_image(screen)
            self.bug_enemy.update()
            self.spray.update()
            self.update_bug_camera(screen)
            self.update_office_resources(screen)

            if self.window_open:
                self.oxygen.update()

            if (
                self.office_state is not office_state.OFFICE_BACK_OPEN
                and self.window_open
            ):
                self.small_bugs.update()
            if (
                self.office_state is not office_state.OFFICE_FRONT_OPEN
                or self.camera_state is not camera_state.NONE
            ) and self.door_open:
                self.small_bugs.update()
            pygame.display.flip()
            framerate_clock.tick(60)
            self.clock.update()
