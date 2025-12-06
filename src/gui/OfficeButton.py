import pygame
from gui.Button import Button
from typing import Callable
class OfficeButton(Button):

    def __init__(self, hue, x, y, width, height, target: Callable):
        super().__init__(width, height, x, y, target)
        #self.__image = pygame.image.load("da")
        self.__hue = hue
        self.__rect = pygame.Rect(x, y, width, height)
        self.__state = False


    def render_button(self,screen: pygame.Surface):
        pygame.draw.rect(screen, self.__hue, self.__rect)

    def getHue(self):
        return self__hue
    def getImage(self):
        return self.__image
    def setHue(self, hue):
        self.__hue = hue
    def setImage(self, image):
        self.__image = image
    def getState(self) -> bool:
        return self.__state

    def mouse_click_handler(self, mouse_position: tuple):

        if mouse_position[0] < self._x:
            return
        if mouse_position[0] > self._x + self._width:
            return
        if mouse_position[1] < self._y:
            return
        if mouse_position[1] > self._y + self._height:
            return
        self.__state = not self.__state
        print("PULA")
