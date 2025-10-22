import pygame
import sys

from src.windows.MainMenu import renderMainMenu

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("5 Nopti In Studentie")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    renderMainMenu(screen, clock, WIDTH, HEIGHT)


pygame.quit()
sys.exit()
