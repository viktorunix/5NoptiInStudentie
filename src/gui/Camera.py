import pygame
from utils.CameraState import CameraState

class Camera:
    def __init__(self, screen_dimension: tuple, script_dir: str):
        self.__width = screen_dimension[0]
        self.__height = screen_dimension[1]
        self.__script_dir = script_dir
        #TODO: add image to import in game
        #self.camera = pygame.image.load(script_dir + "")
    def change_image(self, image: pygame.image):
        self.camera = image
    def render_camera(self, screen, camera_state):
        pass
