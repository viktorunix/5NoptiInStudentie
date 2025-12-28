import pygame

from gui.OfficeButton import OfficeButton
from gui.Picture import image
from utils.office_state import office_state
from utils.stateLoader import get_resource_path


class Office:
    def __init__(self, screen_dimension: tuple, script_dir: str):
        self.__width = screen_dimension[0]
        self.__height = screen_dimension[1]
        self.__script_dir = script_dir
        self.office = pygame.image.load(
            get_resource_path("/assets/images/office_front_lights.jpeg")
        )
        scale_factor = self.__height / self.office.get_height()
        new_width = int(self.office.get_width() * scale_factor)
        print(str(scale_factor) + " " + str(new_width))
        self.office = pygame.transform.scale(self.office, (new_width, self.__height))
        self.office_width = self.office.get_width()
        self.camera_x = 0
        self.scroll_speed = 40

        self.cam_open_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/cam_open.mp3")
        )

        # TODO: trebuie schimbat liniile astea
        self.__camera_button = OfficeButton(
            pygame.Color("red"),
            self.__width / 4,
            self.__height * 9 / 10,
            self.__width / 2,
            self.__height / 20,
            sound=self.cam_open_sound,
        )
        self.__back_office_button = OfficeButton(
            pygame.Color("red"),
            self.__width * 17 / 18,
            self.__height / 4,
            self.__width / 30,
            self.__height / 2,
        )
        # What is this???
        self.__laptop_button = OfficeButton(
            pygame.Color("red"), 100, self.__height - 50, 400, 70
        )
        self.__door_button = OfficeButton(
            pygame.Color("red"),
            self.__width * 17 / 18,
            self.__height / 4,
            self.__width / 30,
            self.__height / 20,
        )
        self.__front_office_button = OfficeButton(
            pygame.Color("red"),
            self.__width / 45,
            self.__height / 4,
            self.__width / 30,
            self.__height / 2,
        )
        self.__front_office_button.change_state()

        self.__window_button = OfficeButton(
            pygame.Color("red"),
            self.__width * 9 / 10,
            self.__height / 4,
            self.__width / 30,
            self.__height / 20,
        )
        run = True
        clock = pygame.time.Clock()
        self.front_office_lights_background = image(
            get_resource_path("/assets/images/office_front_lights.jpeg"),
            screen_dimension,
            1,
        )
        print(screen_dimension)
        self.back_office_lights_background = image(
            get_resource_path("/assets/images/office_back_lights.jpg"),
            screen_dimension,
            1,
        )

        self.front_office_lights_open_background = image(
            get_resource_path("/assets/images/office_front_lights_open.jpg"),
            screen_dimension,
            1,
        )

        self.back_office_lights_open_background = image(
            get_resource_path("/assets/images/office_back_lights_open.jpg"),
            screen_dimension,
            1,
        )

    def test(self, screen, clock):
        print("mergeeee")

    def get_camera_button(self) -> OfficeButton:
        return self.__camera_button

    def get_back_office_button(self) -> OfficeButton:
        return self.__back_office_button

    def get_front_office_button(self) -> OfficeButton:
        return self.__front_office_button

    def get_door_button(self) -> OfficeButton:
        return self.__door_button

    def get_window_button(self) -> OfficeButton:
        return self.__window_button

    def change_image(self, image):
        self.office = image.get_image()

    def render_office(self, screen, office_state):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < 100:
            self.camera_x -= self.scroll_speed
        if mouse_pos[0] > self.__width - 100:
            self.camera_x += self.scroll_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_x -= self.scroll_speed
        if keys[pygame.K_RIGHT]:
            self.camera_x += self.scroll_speed
        self.camera_x = 0 if self.camera_x < 0 else self.camera_x
        self.camera_x = (
            self.office.get_width() - self.__width
            if self.camera_x > self.office.get_width() - self.__width
            else self.camera_x
        )
        view_rect = pygame.Rect(self.camera_x, 0, self.__width, self.__height)
        screen.blit(self.office, (0, 0), view_rect)
        if (
            office_state is office_state.OFFICE_FRONT_LIGHTS
            or office_state is office_state.OFFICE_FRONT_DARK
            or office_state is office_state.OFFICE_FRONT_LIGHTS_OPEN
            or office_state is office_state.OFFICE_FRONT_DARK_OPEN
        ):
            # self.__camera_button.render_button(screen)
            self.__door_button.render_button(screen, scroll_x=self.camera_x)
            if self.camera_x == self.office.get_width() - self.__width:
                self.__back_office_button.render_button(screen)

            if self.camera_x < 30:
                self.__camera_button.render_button(screen)
        if (
            office_state is office_state.OFFICE_BACK_LIGHTS
            or office_state is office_state.OFFICE_BACK_LIGHTS_OPEN
        ):
            if self.camera_x == self.office.get_width() - self.__width:
                self.__window_button.render_button(screen)
            if self.camera_x == 0:
                self.__front_office_button.render_button(screen)
