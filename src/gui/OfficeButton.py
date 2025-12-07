import pygame
from gui.Button import Button
from typing import Callable
class OfficeButton(Button):

    def __init__(self, background: pygame.Color, x, y, width, height, target: Callable=None):
        super().__init__(width, height, x, y, target)
        #self.__image = pygame.image.load("da")
        self.__background = background
        self.__rect = pygame.Rect(x, y, width, height)
        self.__state = True


    def render_button(self,screen: pygame.Surface):
        pygame.draw.rect(screen, self.__background, self.__rect)


    def get_background(self) -> pygame.Color:
        return self.__background
    def get_image(self) -> pygame.image:
        return self.__image
    def set_background(self, background: pygame.Color):
        self.__background = background
    def set_image(self, image):
        self.__image = image
    def get_state(self) -> bool:
        return self.__state
    def change_state(self):
        self.__state = not self.__state
    def mouse_click_handler(self, mouse_position: tuple) -> bool:
        if mouse_position[0] < self._x:
            return False
        if mouse_position[0] > self._x + self._width:
            return False
        if mouse_position[1] < self._y:
            return False
        if mouse_position[1] > self._y + self._height:
            return False
        return True
