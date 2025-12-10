from typing import Callable
import pygame


class Button:
    def __init__(self, screen_dimensions: tuple, position: tuple, target: Callable = None):
        self._width = screen_dimensions[0]
        self._height = screen_dimensions[1]
        self._x = position[0]
        self._y = position[1]
        self._target = target

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_width(self, width: int):
        self._width = width

    def set_height(self, height: int):
        self._height = height

    def set_x(self, x: int):
        self._x = x

    def set_y(self, y: int):
        self._y = y

    def trigger(self):
        self._target()

    def trigger(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self._target(screen, clock)
    def mouse_click_handler(self, mouse_position: tuple,
    screen: pygame.Surface, clock: pygame.time.Clock = None):
        if mouse_position[0] < self.get_x():
            return
        if mouse_position[0] > self.get_x() + self.get_width():
            return
        if mouse_position[1] < self.get_y():
            return
        if mouse_position[1] > self.get_y() + self.get_height():
            return
        if self._target:
            self.trigger(screen, clock)
