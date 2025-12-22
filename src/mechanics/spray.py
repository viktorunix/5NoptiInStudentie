import pygame


class spray:
    def __init__(self, script_dir, max_uses=10):
        self.cooldown_max = 60  # 60 ticks = 1 sec
        self.cooldown_timer = 0
        self.toxicity_penalty = 40  # 40%
        self.max_uses = max_uses
        self.current_uses = max_uses
        try:
            self.sound = pygame.mixer.Sound(script_dir + "/assets/audio/spray.mp3")
        except:
            self.sound = None

    def update(self):
        print(self.cooldown_timer)
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
