import pygame

from src.utils.Deprecated import deprecated


@deprecated
def renderText(screen: pygame.Surface, font: pygame.font.Font, text: str, color: pygame.Color, dest: tuple[float, float]):
    text = font.render(text, True, color)
    text.set_alpha(180)
    screen.blit(text, dest)

def renderTextCenter(screen: pygame.Surface, font: pygame.font.Font, text: str, color: pygame.Color, dest: tuple[float, float]):
    text = font.render(text, True, color)
    text.set_alpha(180)
    textRect = text.get_rect()
    textRect.center = dest
    screen.blit(text, textRect.topleft)