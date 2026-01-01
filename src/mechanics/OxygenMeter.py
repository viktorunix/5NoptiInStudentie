import pygame


class OxygenMeter:
    def __init__(self, max_oxygen, regen_rate, screen_height: int):
        self.max_oxygen = max_oxygen
        self.current_oxygen = max_oxygen
        self.regen_rate = regen_rate
        self.width = screen_height / 5
        self.height = screen_height / 50

    def update(self):
        if self.current_oxygen < self.max_oxygen:
            self.current_oxygen += self.regen_rate
            # hmmmmm
            if self.current_oxygen > self.max_oxygen:
                self.current_oxygen = self.max_oxygen

    def deplete(self, amount):
        self.current_oxygen -= amount
        if self.current_oxygen <= 0:
            self.current_oxygen = 0
            return True
        return False

    def render_bar(self, screen: pygame.Surface, x, y):
        percent = self.current_oxygen / self.max_oxygen
        fill_width = int(self.width * percent)

        if percent > 0.5:
            color = (0, 255, 0)
        elif percent > 0.3:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)

        pygame.draw.rect(screen, (50, 50, 50), (x, y, self.width, self.height))
        pygame.draw.rect(screen, color, (x, y, fill_width, self.height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, self.width, self.height), 2)
