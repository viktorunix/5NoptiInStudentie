import pygame

from utils.stateLoader import get_resource_path


class Spray:
    def __init__(self, max_uses=5):
        self.cooldown_max = 60  # 60 ticks = 1 sec
        self.cooldown_timer = 0
        self.toxicity_penalty = 40  # 40%
        self.max_uses = max_uses
        self.current_uses = max_uses
        self.restock_timer = 0
        self.restock_max = 60 * 20  # 20 sec
        try:
            self.sound = pygame.mixer.Sound(
                get_resource_path("/assets/audio/spray.mp3")
            )
        except:
            self.sound = None

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def use_spray(self) -> bool:
        if self.cooldown_timer > 0:
            return False
        if self.current_uses > 0:
            self.current_uses -= 1
            self.cooldown_timer = self.cooldown_max
            if self.sound:
                self.sound.play()
            return True
        return False

    def get_toxicity(self):
        return self.toxicity_penalty

    def restock(self) -> bool:
        self.restock_timer += 1
        if self.restock_timer >= self.restock_max:
            self.restock_timer = 0
            self.current_uses = self.max_uses
            self.restock_max += (
                60 * 5
            )  # every restock would increase the timer by 5 seconds
            return False
        return True
