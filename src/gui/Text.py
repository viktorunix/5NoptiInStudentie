import pygame



def renderText(screen: pygame.Surface, font: pygame.font.Font, text: str, color: pygame.Color, dest: tuple[float, float]):
    text = font.render(text, True, color)
    text.set_alpha(180)
    screen.blit(text, dest)

