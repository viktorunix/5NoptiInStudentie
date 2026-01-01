import math
import pygame

from utils.stateLoader import get_resource_path
from mechanics.Clock import Clock

class JumpscareAnimation:
    def __init__(self, HEIGHT : int, WIDTH : int):
        self.clock = Clock()
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.jumpscare_sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/jumpscare_sound.mp3")
        )
        unscaled_jmpsc_image = pygame.image.load(
            get_resource_path("/assets/images/mainmenuanimatronic.png")
        )
        scale_factor_bug = self.HEIGHT / 150
        self.jumpscare_image = pygame.transform.scale(
            unscaled_jmpsc_image, (unscaled_jmpsc_image.get_width() * scale_factor_bug,
                                   unscaled_jmpsc_image.get_height() * scale_factor_bug)
        ).convert_alpha()
        unscaled_office_background = pygame.image.load(
            get_resource_path("/assets/images/office_front_lights.jpeg")
        )
        self.jumpscare_animation_frames = self.load()
        scale_factor_office = self.HEIGHT / unscaled_office_background.get_height()
        new_width = int(unscaled_office_background.get_width() * scale_factor_office)
        print(str(scale_factor_office) + " " + str(new_width))
        self.office_background = pygame.transform.scale(unscaled_office_background, (new_width, self.HEIGHT)).convert_alpha()

    def load(self) -> list[pygame.Surface]:
        animation_frames = []
        for i in range(10):
            animation_frame = pygame.transform.scale(
                self.jumpscare_image,
                (self.jumpscare_image.get_width() / (10 - i),
                 self.jumpscare_image.get_height() / (10 - i))
            )
            animation_frames.append(animation_frame)
        for i in range(15):
            animation_frame = pygame.transform.rotate(
                self.jumpscare_image,
                30 * math.sin(i * 2 * math.pi / 15)
            )
            animation_frames.append(animation_frame)
        return animation_frames

    def play(self, screen: pygame.Surface):
        framerate_clock = pygame.time.Clock()
        self.jumpscare_sound.play()
        for i in range(10):
            screen.blit(self.office_background, (0, 0))
            screen.blit(self.jumpscare_animation_frames[i],
                        ((self.WIDTH - self.jumpscare_animation_frames[i].get_width()) / 2,
                         (self.HEIGHT - self.jumpscare_animation_frames[i].get_height() * 0.8) / 2))
            pygame.display.flip()
            framerate_clock.tick(60)
            self.clock.update()

        for j in range(8):
            for i in range(15):
                screen.blit(self.office_background, (0, 0))
                screen.blit(self.jumpscare_animation_frames[i + 10],
                            ((self.WIDTH - self.jumpscare_animation_frames[i + 10].get_width()) / 2,
                             (self.HEIGHT - self.jumpscare_animation_frames[i + 10].get_height() * 0.8) / 2))
                pygame.display.flip()
                framerate_clock.tick(60)
                self.clock.update()
