import threading

import cv2
import pygame
from pygame import Surface
from pygame.time import Clock

from gui import Text


class MainMenu:
    running = True
    def load_assets(self):
        self.cap= cv2.VideoCapture("/mnt/c/Users/Andrei/PycharmProjects/5NoptiInStudentie/assets/videos/mainmenu.mp4")
    def load_audio(self):
        self.sound = pygame.mixer.Sound("/mnt/c/Users/Andrei/PycharmProjects/5NoptiInStudentie/assets/audio/mainmenu.mp3")
        self.channel.play(self.sound,-1)
    def loader(self):
        loader_thread = threading.Thread(target =self.load_assets)
        loader_thread.start()
        #self.load_assets()
        loader_audio_thread = threading.Thread(target = self.load_audio)
        loader_audio_thread.start()

    def __init__(self, WIDTH: int, HEIGHT: int):
        self.sound = None
        self.WIDTH= WIDTH
        self.HEIGHT =HEIGHT
        self.cap: cv2.VideoCapture = cv2.VideoCapture()
        self.channel = pygame.mixer.find_channel()
        self.another_channel = pygame.mixer.find_channel()
        self.bugimage = pygame.image.load("/mnt/c/Users/Andrei/PycharmProjects/5NoptiInStudentie/assets/images/mainmenuanimatronic.png").convert_alpha()
        self.bugimage.set_alpha(180)
        self.bugimage = pygame.transform.scale(self.bugimage,(self.bugimage.get_width()*2, self.bugimage.get_height() * 2))

    def warningScreen(self, screen: Surface, clock: Clock):
        loaded = False
        self.loader()
        easter_egg_sound = pygame.mixer.Sound("/mnt/c/Users/Andrei/PycharmProjects/5NoptiInStudentie/assets/audio/easteregg.mp3")
        #another_channel = pygame.mixer.find_channel()
        self.another_channel.play(easter_egg_sound)
        print(self.another_channel.get_busy())
        while not loaded:
            print(self.another_channel.get_busy())
            ret, frame = self.cap.read()
            if ret or not self.another_channel.get_busy():
                loaded = True
            #image = pygame.image.load("/mnt/c/Users/Andrei/PycharmProjects/5NoptiInStudentie/assets/images/warningscreen.jpeg")
            #image = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
            #image.set_alpha(120)
            #screen.blit(image,(0,0))
            font = pygame.font.Font(None, 74)
            text = font.render("ATENTIE!!", True, (255, 0, 0))
            screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT/2 +50))
            text = font.render("URMEAZA IMAGINI CU IMPACT EMOTIONAL", True, (255, 0, 0))
            screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2,  self.HEIGHT/2+100))
            text = font.render("bazat pe o poveste reala", True, (255, 0, 0))
            screen.blit(text, (self.WIDTH / 2 - text.get_width() / 2,  self.HEIGHT/2+150))
            pygame.display.flip()
            clock.tick(60)

    def renderMainMenu(self, screen: Surface, clock: Clock):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0,1))
            screen.blit(frame,(0,0))
            font = pygame.font.Font(None, 74)

            Text.renderText(screen, font, "Cinci ", (255, 255, 255), (50, 50))
            Text.renderText(screen, font, "Nopti", (255, 255, 255), (50, 80 + 74/2))
            Text.renderText(screen, font, "In", (255, 255, 255), (50, 110 + 74))
            Text.renderText(screen, font, "Studentie", (255,255,255), (50, 140 + 74 * 1.5))

            Text.renderText(screen, font, "New Game", (255,255,255), (50, 350 + 74 / 2))
            Text.renderText(screen, font, "Continue", (255,255,255), (50, 450 + 74 / 2))

            screen.blit(self.bugimage,(700, -200))
            pygame.display.flip()
            clock.tick(60)