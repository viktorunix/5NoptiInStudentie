import pygame

from src.utils.Deprecated import deprecated

class Text:
    font: pygame.font.Font
    screen: pygame.Surface
    def __init__(self, screen: pygame.Surface, fontPath:str=None, fontSize:int=74):
        self.screen = screen
        self.font = pygame.font.Font(fontPath, fontSize)

    def renderText(self, text: str, color: pygame.Color, dest:tuple, center=False):
        text = self.font.render(text, True, color)
        text.set_alpha(180)
        if center:
            textRect = text.get_rect()
            textRect.center = dest
            self.screen.blit(text, textRect.topleft)
        else:
            self.screen.blit(text, dest)

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