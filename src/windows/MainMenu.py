import pygame
from pygame import Surface
from pygame.time import Clock


def renderMainMenu(screen: Surface, clock: Clock, WIDTH: int, HEIGHT: int):
    # Update game logic here

    # Draw
    screen.fill((0,0,0));
    

    # Example: display text
    font = pygame.font.Font(None, 74)
    text = font.render("Cinci nopti in", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    text = font.render("studentie", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + text.get_height() // 2 + 30))

    # Flip the display
    pygame.display.flip()
    clock.tick(60)
