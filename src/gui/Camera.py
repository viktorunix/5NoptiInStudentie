import cv2
import pygame

from gui.OfficeButton import OfficeButton
from gui.Picture import image
from gui.Text import Text
from gui.VideoBackground import VideoBackground
from utils.game_state import camera_state
from utils.stateLoader import get_resource_path


class Camera:
    """Class for rendering and defining each UI component for the camera surveillance mechanic"""

    def __init__(
        self, screen_dimension: tuple, video_background: VideoBackground = None
    ):
        self.cap = cv2.VideoCapture(get_resource_path("/assets/videos/mainmenu.mp4"))
        self.__width = screen_dimension[0]
        self.__height = screen_dimension[1]
        self.video_background = video_background
        self.cam_close_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/cam_close.mp3")
        )
        # TODO: add image to import in game
        self.camera = pygame.image.load(
            get_resource_path("/assets/images/main_hallway_a.jpg")
        )

        self.cam_switch_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/cam_switch.mp3")
        )

        scale_factor = self.__height / self.camera.get_height()
        new_width = int(self.camera.get_width() * scale_factor)
        self.camera = pygame.transform.scale(
            self.camera, (new_width * 1.50, self.__height)
        )
        self.office_button = OfficeButton(
            pygame.Color("red"),
            self.__width / 4,
            self.__height * 9 / 10,
            self.__width / 2,
            self.__height / 20,
            sound=self.cam_close_sound,
            cam=True,
            text="Close",
        )
        horizontalOffset = self.__width * 2 / 3
        verticalOffset = self.__height * 4 / 5
        horizontalSize = self.__width / 28
        verticalSize = self.__height / 20

        self.bath_hallway_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="1A",
            sound=self.cam_switch_sound,
        )
        self.main_hallway_a_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 2 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="2A",
            sound=self.cam_switch_sound,
        )
        self.main_hallway_office_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 3.5 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="2B",
            sound=self.cam_switch_sound,
        )
        self.main_hallway_b_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 5 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="2C",
            sound=self.cam_switch_sound,
        )
        self.staircase_button = OfficeButton(
            pygame.Color("white"),
            horizontalOffset + 7 * horizontalSize,
            verticalOffset,
            horizontalSize,
            verticalSize,
            cam=True,
            text="3A",
            sound=self.cam_switch_sound,
        )
        self.restock_spray_button = OfficeButton(
            pygame.Color("white"),
            screen_dimension[0] / 9,
            screen_dimension[1] / 9,
            horizontalSize * 3,
            verticalSize,
            cam=True,
            text="Restock",
            sound=None,
        )
        self.staircase_background = image(
            get_resource_path("/assets/images/staircase.jpg"), screen_dimension, 1
        )
        self.main_hallway_a_background = image(
            get_resource_path("/assets/images/main_hallway_a.jpg"), screen_dimension, 1
        )
        self.main_hallway_b_background = image(
            get_resource_path("/assets/images/main_hallway_b.jpg"), screen_dimension, 1
        )
        self.bath_hallway_background = image(
            get_resource_path("/assets/images/bath_hallway.jpg"), screen_dimension, 1
        )
        self.main_hallway_office_background = image(
            get_resource_path("/assets/images/main_hallway_office.jpg"),
            screen_dimension,
            1,
        )

        self.bath_hallway_bug_background = image(
            get_resource_path("/assets/images/bath_hallway_bug.jpg"),
            screen_dimension,
            1,
        )
        self.main_hallway_a_bug_background = image(
            get_resource_path("/assets/images/main_hallway_a_bug.jpg"),
            screen_dimension,
            1,
        )
        self.main_hallway_b_bug_background = image(
            get_resource_path("/assets/images/main_hallway_b_bug.jpg"),
            screen_dimension,
            1,
        )
        self.main_hallway_office_bug_background = image(
            get_resource_path("/assets/images/main_hallway_office_bug.jpg"),
            screen_dimension,
            1,
        )

        self.staircase_bug_background = image(
            get_resource_path("/assets/images/staircase_bug.jpg"),
            screen_dimension,
            1,
        )

    def change_image(self, image):
        self.camera = image.get_image()

    def render_camera(self, screen, camera_state_player, alpha: int):
        screen.blit(self.camera, (0, 0))
        self.video_background.static_update(screen, alpha)
        # self.static_update(screen, alpha)

        horizontalOffset = self.__width * 2 / 3
        verticalOffset = self.__height * 4 / 5
        horizontalSize = self.__width / 28
        verticalSize = self.__height / 20
        player_marker_text = Text(screen)
        player_marker_text.renderText(
            "You",
            "white",
            (
                self.main_hallway_office_button.get_x()
                + self.main_hallway_office_button.get_width() / 2,
                self.main_hallway_office_button.get_y() * 15 / 16,
            ),
            True,
        )
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
        self.office_button.render_button(screen)
        self.main_hallway_a_button.render_button(screen)
        self.bath_hallway_button.render_button(screen)
        self.main_hallway_b_button.render_button(screen)
        self.staircase_button.render_button(screen)
        self.main_hallway_office_button.render_button(screen)
        if camera_state_player in [camera_state.STAIRWAY, camera_state.STAIRWAY_BUG]:
            self.restock_spray_button.render_button(screen)

    def static_update(self, screen: pygame.Surface, alpha: int):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        frame = cv2.resize(frame, (self.__width, self.__height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame.set_alpha(alpha)
        screen.blit(frame, (0, 0))
