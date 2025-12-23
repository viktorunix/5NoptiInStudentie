from typing import Callable

import pygame

from gui.Button import Button
from gui.Text import Text


class OfficeButton(Button):
    def __init__(
        self,
        background: pygame.Color,
        x,
        y,
        width,
        height,
        target: Callable = None,
        text: str = "",
        cam: bool = False,
    ):
        super().__init__((width, height), (x, y), target)
        # self.__image = pygame.image.load("da")
        self.__background = background
        self.__rect = pygame.Rect(x, y, width, height)
        self.__state = True
        self.__cam = cam
        self.__text = text

    def render_button(self, screen: pygame.Surface):
        if not self.__cam:
            pygame.draw.rect(screen, self.__background, self.__rect)
        else:
            # pygame.draw.rect(screen, self.__background, self.__rect)
            # pygame.draw.rect(
            #    screen,
            #    pygame.Color("black"),
            #    (
            #        self.__rect.x + 5,
            #        self.__rect.y + 5,
            #        self.__rect.width - 10,
            #        self.__rect.height - 10,
            #    ),
            # )
            pygame.draw.rect(screen, self.__background, self.__rect, 5)
            text = Text(screen)
            text.renderText(
                self.__text,
                "white",
                (
                    self.__rect.x + self.__rect.width / 2,
                    self.__rect.y + self.__rect.height / 2,
                ),
                True,
            )

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
