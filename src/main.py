import os
import sys
import warnings

import pygame

from gui.OfficeButton import OfficeButton
from windows.MainGame import MainGame
from windows.MainMenu import MainMenu

warnings.simplefilter("always", DeprecationWarning)


def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Screen setup
    info = pygame.display.Info()
    WIDTH = info.current_w
    HEIGHT = info.current_h
    # WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    clock = pygame.time.Clock()
    clock = pygame.time.Clock()
    pygame.display.set_caption("5 Nopti In Studentie")

    # Clock
    clock = pygame.time.Clock()
    FPS = 60

    # Colors

    # Game loop

    menu = MainMenu(WIDTH, HEIGHT)
    menu.loader()

    menu.warningScreen(screen, clock)
    menu.renderMainMenu(screen, clock)
    # main_game = MainGame(WIDTH, HEIGHT)
    # main_game.loadingScreen(screen, clock)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
