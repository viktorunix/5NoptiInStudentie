import pygame

class image:
    """image gui component class"""
    def __init__(self, file_path: str, screen_dimension: tuple, horizontal_stretch: float = 1.50):
        self.__image = pygame.image.load(file_path)
        scale_factor = screen_dimensions[1] / self.__image.get_height()
        new_width = int(self.__image.get_width() * scale_factor)
            self.__image = pygame.transform.scale(self.__image, (new_width * horizontal_stretch, screen_dimensions[1]))
