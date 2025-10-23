import pygame
import cv2
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

cap = cv2.VideoCapture("/mnt/c/Users/Andrei/PycharmProjects/5NoptiInStudentie/assets/videos/mainmenu.mp4")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0,1))
    screen.blit(frame,(0,0))
    renderMainMenu(screen, clock, WIDTH, HEIGHT)
    if(not channel.get_busy()):
        channel.play(sound)

    pygame.display.flip()
    clock.tick(60)
cap.release()
pygame.quit()
sys.exit()
