import cv2
import pygame

from gui.OfficeButton import OfficeButton
from gui.Picture import image
from utils.camera_state import camera_state


class Camera:
    """Class for rendering and defining each UI component for the camera surveillance mechanic"""

    def __init__(self, screen_dimension: tuple, script_dir: str):
        self.cap = cv2.VideoCapture(script_dir + "/assets/videos/mainmenu.mp4")
        self.__width = screen_dimension[0]
        self.__height = screen_dimension[1]
        self.__script_dir = script_dir
        self.cam_close_sound = pygame.mixer.Sound(
            script_dir + "/assets/audio/cam_close.mp3"
        )
        # TODO: add image to import in game
        self.camera = pygame.image.load(
            script_dir + "/assets/images/main_hallway_a.jpg"
        )

        self.cam_switch_sound = pygame.mixer.Sound(
            script_dir + "/assets/audio/cam_switch.mp3"
        )

        scale_factor = self.__height / self.camera.get_height()
        new_width = int(self.camera.get_width() * scale_factor)
        self.camera = pygame.transform.scale(
            self.camera, (new_width * 1.50, self.__height)
        )
        self.__office_button = OfficeButton(
            pygame.Color("red"),
            self.__width / 4,
            self.__height * 9 / 10,
            self.__width / 2,
            self.__height / 20,
            sound=self.cam_close_sound,
        )
        horizontalOffset = self.__width * 2 / 3
        verticalOffset = self.__height * 4 / 5
        horizontalSize = self.__width / 28
        verticalSize = self.__height / 20
        self.__bath_hallway_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="1A",
            sound=self.cam_switch_sound,
        )
        self.__main_hallway_a_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 2 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="2A",
            sound=self.cam_switch_sound,
        )
        self.__main_hallway_office_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 3.5 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="2B",
            sound=self.cam_switch_sound,
        )
        self.__main_hallway_b_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 5 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="2C",
            sound=self.cam_switch_sound,
        )
        self.__staircase_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 7 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="3A",
            sound=self.cam_switch_sound,
        )
        self.staircase_background = image(
            script_dir + "/assets/images/staircase.jpg", screen_dimension, 1
        )
        self.main_hallway_a_background = image(
            script_dir + "/assets/images/main_hallway_a.jpg", screen_dimension, 1
        )
        self.main_hallway_b_background = image(
            script_dir + "/assets/images/main_hallway_b.jpg", screen_dimension, 1
        )
        self.bath_hallway_background = image(
            script_dir + "/assets/images/bath_hallway.jpg", screen_dimension, 1
        )
        self.main_hallway_office_background = image(
            script_dir + "/assets/images/main_hallway_office.jpg", screen_dimension, 1
        )

        self.bath_hallway_bug_background = image(
            script_dir + "/assets/images/bath_hallway_bug.jpg", screen_dimension, 1
        )
        self.main_hallway_a_bug_background = image(
            script_dir + "/assets/images/main_hallway_a_bug.jpg", screen_dimension, 1
        )
        self.main_hallway_b_bug_background = image(
            script_dir + "/assets/images/main_hallway_b_bug.jpg", screen_dimension, 1
        )
        self.main_hallway_office_bug_background = image(
            script_dir + "/assets/images/main_hallway_office_bug.jpg",
            screen_dimension,
            1,
        )

        self.staircase_bug_background = image(
            script_dir + "/assets/images/staircase_bug.jpg",
            screen_dimension,
            1,
        )

    def change_image(self, image):
        self.camera = image.get_image()

    def get_office_button(self) -> OfficeButton:
        return self.__office_button

    def get_main_hallway_a_button(self) -> OfficeButton:
        return self.__main_hallway_a_button

    def get_bath_hallway_button(self) -> OfficeButton:
        return self.__bath_hallway_button

    def get_staircase_button(self) -> OfficeButton:
        return self.__staircase_button

    def get_main_hallway_b_button(self) -> OfficeButton:
        return self.__main_hallway_b_button

    def get_main_hallway_office_button(self) -> OfficeButton:
        return self.__main_hallway_office_button

    def render_camera(self, screen, camera_state):
        screen.blit(self.camera, (0, 0))
        self.static_update(screen)

        horizontalOffset = self.__width * 2 / 3
        verticalOffset = self.__height * 4 / 5
        horizontalSize = self.__width / 28
        verticalSize = self.__height / 20

        # main hallway
        pygame.draw.rect(
            screen,
            pygame.Color("white"),
            (
                horizontalOffset + horizontalSize * 1.75,
                verticalOffset - verticalSize / 4,
                horizontalSize * 4.5,
                verticalSize * 1.5,
            ),
            2,
        )
        # bathroom hallway
        pygame.draw.rect(
            screen,
            pygame.Color("white"),
            (
                horizontalOffset - horizontalSize * 0.25,
                verticalOffset - verticalSize / 4,
                horizontalSize * 1.5,
                verticalSize * 1.5,
            ),
            2,
        )
        # staircase
        pygame.draw.rect(
            screen,
            pygame.Color("white"),
            (
                horizontalOffset + horizontalSize * 6.75,
                verticalOffset - verticalSize / 4,
                horizontalSize * 1.5,
                verticalSize * 1.5,
            ),
            2,
        )
        """pygame.draw.rect(
            screen,
            pygame.Color("white"),
            (self.__width - 900, self.__height - 280, 50, 30),
            2,
        )"""
        """pygame.draw.rect(
            screen,
            pygame.Color("white"),
            (self.__width - 450, self.__height - 280, 50, 30),
            2,
        )"""
        self.__office_button.render_button(screen)
        self.__main_hallway_a_button.render_button(screen)
        self.__bath_hallway_button.render_button(screen)
        self.__main_hallway_b_button.render_button(screen)
        self.__staircase_button.render_button(screen)
        self.__main_hallway_office_button.render_button(screen)

    def static_update(self, screen: pygame.Surface):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        frame = cv2.resize(frame, (self.__width, self.__height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame.set_alpha(64)
        screen.blit(frame, (0, 0))
