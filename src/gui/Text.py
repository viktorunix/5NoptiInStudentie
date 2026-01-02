import pygame


class Text:
    font: pygame.font.Font
    screen: pygame.Surface

    def __init__(
        self, screen: pygame.Surface, fontPath: str = None, fontSize: int = 74
    ):
        self.screen = screen
        # taking the width of my screen as reference not really an ok solution but works for now
        aux_width = 2880
        screen_width = pygame.display.Info()
        scale_factor = screen_width.current_w / aux_width
        # scale_factor = scale_factor if scale_factor < 1 else 1 / scale_factor
        fontSize = int(fontSize * scale_factor)
        self.font = pygame.font.Font(fontPath, fontSize)
        self.fontSize = fontSize

    def renderText(self, message: str, color, dest: tuple, center=False):
        if type(color) is str:
            color = pygame.Color(color)
        text = self.font.render(message, True, color)
        text.set_alpha(180)
        if center:
            textRect = text.get_rect()
            textRect.center = dest
            self.screen.blit(text, textRect.topleft)
        else:
            self.screen.blit(text, dest)

    def getSize(self):
        return self.fontSize
