import pygame
from utils.CameraState import CameraState
from gui.OfficeButton import OfficeButton
class Camera:
    """Class for rendering and defining each UI component for the camera surveillance mechanic"""
    def __init__(self, screen_dimension: tuple, script_dir: str):
        self.__width = screen_dimension[0]
        self.__height = screen_dimension[1]
        self.__script_dir = script_dir
        #TODO: add image to import in game
        self.camera = pygame.image.load(script_dir + "/assets/images/main_hallway_a.jpg")
        scale_factor = self.__height / self.camera.get_height()
        new_width = int(self.camera.get_width() * scale_factor)
        self.camera = pygame.transform.scale(self.camera, (new_width * 1.50, self.__height))
        self.__office_button = OfficeButton(pygame.Color("red"), self.__width - 600, self.__height - 120, 500, 100)
        self.__main_hallway_a_button = OfficeButton(pygame.Color("red"), self.__width - 900, self.__height - 300, 80, 80)
        self.__bath_hallway_button = OfficeButton(pygame.Color("red"), self.__width - 800, self.__height - 300, 80, 80)
        self.__main_hallway_b_button = OfficeButton(pygame.Color("red"), self.__width - 700, self.__height - 300, 80, 80)
        self.__staircase_button = OfficeButton(pygame.Color("red"), self.__width - 600, self.__height - 300, 80, 80)

    def change_image(self, image: pygame.image):
        self.camera = image

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
    def render_camera(self, screen, camera_state):
        screen.blit(self.camera, (0, 0))
        self.__office_button.render_button(screen)
        self.__main_hallway_a_button.render_button(screen)
        self.__bath_hallway_button.render_button(screen)
        self.__main_hallway_b_button.render_button(screen)
        self.__staircase_button.render_button(screen)

