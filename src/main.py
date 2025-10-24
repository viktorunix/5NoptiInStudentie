
import pygame
import sys
from windows.MainMenu import  MainMenu

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

menu = MainMenu(WIDTH, HEIGHT)
menu.loader()

menu.warningScreen(screen, clock)
menu.renderMainMenu(screen,clock)
pygame.quit()
sys.exit()
