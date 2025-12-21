import os
import sys
import warnings

import pygame

from gui.OfficeButton import OfficeButton
from windows.MainGame import MainGame
from windows.MainMenu import MainMenu

warnings.simplefilter("always", DeprecationWarning)


def main():
    button: OfficeButton = OfficeButton(2, 2, 2, 2, 2, main)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = script_dir[:-4]
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    # Screen setup
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("5 Nopti In Studentie")

    # Clock
    clock = pygame.time.Clock()
    FPS = 60

    # Colors

    # Game loop

    menu = MainMenu(WIDTH, HEIGHT, script_dir)
    menu.loader()

    menu.warningScreen(screen, clock)
    menu.renderMainMenu(screen, clock)
    # main_game = MainGame(WIDTH, HEIGHT)
    # main_game.loadingScreen(screen, clock)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
