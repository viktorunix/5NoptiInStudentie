import pygame
import sys

from windows.MainMenu import renderMainMenu

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
BLACK = (0, 0, 0)

# Game loop
running = True
sound = pygame.mixer.Sound("/mnt/c/Users/Andrei/PycharmProjects/5NoptiInStudentie/assets/audio/mainmenu.mp3")
channel = pygame.mixer.find_channel()
channel.play(sound)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    renderMainMenu(screen, clock, WIDTH, HEIGHT)
    if(not channel.get_busy()):
        channel.play(sound)


pygame.quit()
sys.exit()
