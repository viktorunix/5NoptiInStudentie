import pygame

from gui.OfficeButton import OfficeButton
from gui.Picture import image
from utils.office_state import office_state


class Office:
    def __init__(self, screen_dimension: tuple, script_dir: str):
        self.__width = screen_dimension[0]
        self.__height = screen_dimension[1]
        self.__script_dir = script_dir
        self.office = pygame.image.load(
            script_dir + "/assets/images/office_front_lights.jpeg"
        )
        scale_factor = self.__height / self.office.get_height()
        new_width = int(self.office.get_width() * scale_factor)
        print(str(scale_factor) + " " + str(new_width))
        self.office = pygame.transform.scale(self.office, (new_width, self.__height))
        self.office_width = self.office.get_width()
        self.camera_x = 0
        self.scroll_speed = 40
        # TODO: trebuie schimbat liniile astea
        self.__camera_button = OfficeButton(
            pygame.Color("red"), self.__width - 600, self.__height - 120, 500, 100
        )
        self.__back_office_button = OfficeButton(
            pygame.Color("red"), 50, self.__height - 700, 100, 500
        )
        self.__laptop_button = OfficeButton(
            pygame.Color("red"), self.__width - 1200, self.__height - 120, 500, 100
        )
        self.__front_office_button = OfficeButton(
            pygame.Color("red"), self.__width - 150, self.__height - 700, 100, 500
        )
        self.__front_office_button.change_state()
        run = True
        clock = pygame.time.Clock()
        self.front_office_lights_background = image(
            script_dir + "/assets/images/office_front_lights.jpeg", screen_dimension, 1
        )
        print(screen_dimension)
        self.back_office_lights_background = image(
            script_dir + "/assets/images/office_back_lights.jpg", screen_dimension, 1
        )

    def test(self, screen, clock):
        print("mergeeee")

    def get_camera_button(self) -> OfficeButton:
        return self.__camera_button

    def get_back_office_button(self) -> OfficeButton:
        return self.__back_office_button

    def get_laptop_button(self) -> OfficeButton:
        return self.__laptop_button

    def get_front_office_button(self) -> OfficeButton:
        return self.__front_office_button

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
        print(str(self.camera_x) + " " + str(self.office.get_width()))
        view_rect = pygame.Rect(self.camera_x, 0, self.__width, self.__height)
        screen.blit(self.office, (0, 0), view_rect)
        if (
            office_state is office_state.OFFICE_FRONT_LIGHTS
            or office_state is office_state.OFFICE_FRONT_DARK
        ):
            self.__camera_button.render_button(screen)
            self.__laptop_button.render_button(screen)
            if self.camera_x == 0:
                self.__back_office_button.render_button(screen)
        if (
            office_state is office_state.OFFICE_BACK_LIGHTS
            or office_state is office_state.OFFICE_BACK_DARK
        ):
            if self.camera_x == self.office.get_width() - self.__width:
                self.__front_office_button.render_button(screen)
