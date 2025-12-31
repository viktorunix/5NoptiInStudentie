import cv2
import pygame


class VideoBackground:
    def __init__(self, filepath, width, height):
        self.frames = []
        self.frame_index = 0
        self.last_update = 0
        self.fps = 30

        cap = cv2.VideoCapture(filepath)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            surf = pygame.image.frombuffer(frame.tobytes(), (width, height), "RGB")
            self.frames.append(surf.convert())
        cap.release()

    def static_update(self, screen, alpha=255):
        if not self.frames:
            return

        now = pygame.time.get_ticks()
        if now - self.last_update > (1000 / self.fps):
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update = now
        current_frame = self.frames[self.frame_index]
        if alpha < 255:
            current_frame.set_alpha(alpha)
        screen.blit(current_frame, (0, 0))
