import pygame
import sys

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

    # Update game logic here

    # Draw
    screen.fill(BLACK)

    # Example: display text
    font = pygame.font.Font(None, 74)
    text = font.render("Office View", True, (255, 255, 255))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

    # Flip the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
