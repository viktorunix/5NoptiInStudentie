import pygame


class spray:
    def __init__(self, script_dir):
        self.cooldown_max = 60  # 60 ticks = 1 sec
        self.cooldown_timer = 0
        try:
            self.sound = pygame.mixer.Sound(script_dir + "/assets/audio/spray.mp3")
        except:
            self.sound = None

    def update(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def use_spray(self) -> bool:
        if self.cooldown_timer == 0:
            self.cooldown_timer = self.cooldown_timer
            if self.sound:
                self.sound.play()
            print("Psst used spray.")
            return True
        else:
            print("spray is on cooldown!")
            return False
