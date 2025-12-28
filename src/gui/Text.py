import pygame


class Text:
    font: pygame.font.Font
    screen: pygame.Surface

    def __init__(
        self, screen: pygame.Surface, fontPath: str = None, fontSize: int = 74
    ):
        self.screen = screen
        self.font = pygame.font.Font(fontPath, fontSize)
        self.fontSize = fontSize

    def renderText(self, text: str, color, dest: tuple, center=False):
        if type(color) == str:
            color = pygame.Color(color)
        text = self.font.render(text, True, color)
        text.set_alpha(180)
        if center:
            textRect = text.get_rect()
            textRect.center = dest
            self.screen.blit(text, textRect.topleft)
        else:
            self.screen.blit(text, dest)

    def getSize(self):
        return self.fontSize
