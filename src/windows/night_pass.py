import cv2
import pygame

from gui.Text import Text
from mechanics.clock import clock
from utils.stateLoader import get_resource_path


class night_pass:
    def __init__(
        self, screen: pygame.Surface, screen_dimensions: tuple, script_dir: str
    ):
        print("night pass lol what do you expect")
        self.screen_dimensions = screen_dimensions
        self.clock = clock()
        self.sound = pygame.mixer.Sound(
            get_resource_path("/assets/audio/night_pass.mp3")
        )
        self.cap = cv2.VideoCapture(get_resource_path("/assets/videos/night_pass.mov"))

    def update(self, screen: pygame.Surface):
        print(self.screen_dimensions)
        running = True
        framerate_clock = pygame.time.Clock()
        self.sound.play()
        while running:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            frame = cv2.resize(
                frame, (self.screen_dimensions[0], self.screen_dimensions[1])
            )
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame.set_alpha(128)
            screen.blit(frame, (0, 0))
            if self.clock.get_seconds() == 5:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False

            print("testing")
            pygame.display.flip()
            self.clock.update()
            framerate_clock.tick(30)
