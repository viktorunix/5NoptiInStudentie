import threading

import cv2
import pygame
from pygame import Surface
from pygame.time import Clock

from gui import Text

# from gui import Button
from gui.Button import Button

from windows.MainGame import MainGame


class MainMenu:
    running = True
    buttons = []

    def load_assets(self):
        self.cap = cv2.VideoCapture(self.script_dir + "/assets/videos/mainmenu.mp4")

    def load_audio(self):
        self.sound = pygame.mixer.Sound(self.script_dir + "/assets/audio/mainmenu.mp3")
        self.channel.play(self.sound, -1)

    def loader(self):
        loader_thread = threading.Thread(target=self.load_assets)
        loader_thread.start()
        # self.load_assets()
        loader_audio_thread = threading.Thread(target=self.load_audio)
        loader_audio_thread.start()

    def __init__(self, WIDTH: int, HEIGHT: int, script_dir):
        self.script_dir = script_dir
        self.sound = None
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.cap: cv2.VideoCapture = cv2.VideoCapture()
        self.channel = pygame.mixer.find_channel()
        self.another_channel = pygame.mixer.find_channel()
        self.bugimage = pygame.image.load(
            self.script_dir + "/assets/images/mainmenuanimatronic.png"
        ).convert_alpha()
        self.bugimage.set_alpha(180)
        self.bugimage = pygame.transform.scale(
            self.bugimage,
            (self.bugimage.get_width() * 2, self.bugimage.get_height() * 2),
        )
        self.buttons.append(Button(250, 50, 50, 350 + 74 / 2, self.event_test))
        self.buttons.append(Button(200, 50, 50, 450 + 74 / 2, self.event_test_altu))

    def renderButtons(self, screen: Surface):
        for button in self.buttons:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (
                    button.get_x(),
                    button.get_y(),
                    button.get_width(),
                    button.get_height(),
                ),
            )

    def warningScreen(self, screen: Surface, clock: Clock):
        loaded = False
        self.loader()
        easter_egg_sound = pygame.mixer.Sound(
            self.script_dir + "/assets/audio/easteregg.mp3"
        )
        # another_channel = pygame.mixer.find_channel()
        self.another_channel.play(easter_egg_sound)
        while not loaded:
            #print(self.another_channel.get_busy())
            ret, frame = self.cap.read()
            if ret and not self.another_channel.get_busy():
                loaded = True
            image = pygame.image.load(
                self.script_dir + "/assets/images/warningscreen.jpeg"
            )
            image = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
            image.set_alpha(120)
            screen.blit(image, (0, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("ATENTIE!!", True, pygame.Color("red"))
            screen.blit(
                text, (self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT / 2 + 50)
            )
            text = font.render("URMEAZA IMAGINI CU IMPACT EMOTIONAL", True, pygame.Color("red"))
            screen.blit(
                text, (self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT / 2 + 100)
            )
            text = font.render("bazat pe o poveste reala", True, pygame.Color("red"))
            screen.blit(
                text, (self.WIDTH / 2 - text.get_width() / 2, self.HEIGHT / 2 + 150)
            )
            pygame.display.flip()
            clock.tick(60)

    def event_test(self, screen: Surface, clock: Clock):
        mainGame = MainGame(self.WIDTH, self.HEIGHT)
        mainGame.loadingScreen(screen, clock)

    def event_test_altu(self):
        print("merge si asta")



    def renderMainMenu(self, screen: Surface, clock: Clock):
        text = Text.Text(screen, None,74)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        button.mouse_click_handler(event.pos, screen, clock)
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame, (0, 0))
            font = pygame.font.Font(None, 74)
            Text.renderText(screen, font, "Cinci ", pygame.Color("white"), (50, 50))
            Text.renderText(screen, font, "Nopti", pygame.Color("white"), (50, 80 + 74 / 2))
            Text.renderText(screen, font, "In", pygame.Color("white"), (50, 110 + 74))
            Text.renderText(screen, font, "Studentie", pygame.Color("white"), (50, 140 + 74 * 1.5))

            Text.renderText(screen, font, "New Game", pygame.Color("white"), (50, 350 + 74 / 2))
            Text.renderText(screen, font, "Continue", pygame.Color("white"), (50, 450 + 74 / 2))

            screen.blit(self.bugimage, (700, -200))

            #Text.renderTextCenter(screen, font, "V0.1indev", pygame.Color("white"), (1030, 680))
            text.renderText( "V0.1indev", pygame.Color("white"), (1030, 680))
            #self.renderButtons(screen)
            pygame.display.flip()
            clock.tick(60)
