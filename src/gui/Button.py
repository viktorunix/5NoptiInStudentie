from typing import Callable


class Button:

    def __init__(self, width: int, height: int, x:int, y:int, target: Callable):
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y
        self.__target = target


    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y

    def set_width(self, width: int):
        self.__width = width
    def set_height(self, height: int):
        self.__height = height
    def set_x(self, x: int):
        self.__x = x
    def set_y(self, y: int):
        self.__y = y


    def trigger(self):
        self.__target()
