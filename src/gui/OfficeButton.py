import pygame
from gui.Button import Button
from typing import Callable
class OfficeButton(Button):

    def __init__(self, hue, x, y, width, height, target: Callable):
        super().__init__(width, height, x, y, target)
        #self.__image = pygame.image.load("da")
        self.__hue = hue
        self.__rect = pygame.Rect(x, y, width, height)
        #print(str(self._x))
    
    def render_button(self,screen: pygame.Surface):
        pygame.draw.rect(screen, self.__hue, self.__rect)

    def getHue():
        return self__hue
    def getImage():
        return self.__image
    def setHue(hue):
        self.__hue = hue
    def setImage(image):
        self.__image = image
