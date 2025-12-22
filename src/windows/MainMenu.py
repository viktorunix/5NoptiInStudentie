import threading

import cv2
import pygame
from pygame import Surface
from pygame.time import Clock

from gui import Text
from gui.Button import Button
from windows.MainGame import MainGame


class MainMenu:
    running = True
    buttons = []

    def load_assets(self):
        self.cap = cv2.VideoCapture(self.script_dir + "/assets/videos/mainmenu.mp4")

    def loader(self):
        self.load_assets()

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

        self.buttons.append(Button((250, 50), (50, 350 + 74 / 2), self.event_test))
        self.buttons.append(Button((200, 50), (50, 450 + 74 / 2), self.event_test_altu))

        self.sound = pygame.mixer.Sound(self.script_dir + "/assets/audio/mainmenu.mp3")

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
        # TOOO: fix bug regarding the sounds not playing
        easter_egg_sound = pygame.mixer.Sound(
            self.script_dir + "/assets/audio/easteregg.mp3"
        )
        self.another_channel = pygame.mixer.find_channel()
        self.another_channel.play(easter_egg_sound)
        text = Text.Text(screen, None, 45)
        is_enter: bool = False
        while not loaded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_enter = True
            ret, frame = self.cap.read()
            if is_enter:
                loaded = True
            try:
                image = pygame.image.load(
                    self.script_dir + "/assets/images/warningscreen.jpeg"
                )
                image = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
                image.set_alpha(120)
                screen.blit(image, (0, 0))
                font = pygame.font.Font(None, 30)
            except Exception as e:
                print("Warning screen background image not found")
            text.renderText(
                "ATENTIE!!", "red", (self.WIDTH / 2, self.HEIGHT / 2 - 200), True
            )
            text.renderText(
                "Acest joc este o parodie si trebuie tratat ca atare",
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 - 50),
                True,
            )
            text.renderText(
                "Urmeaza imagini care pot afecta emotional",
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2),
                True,
            )
            text.renderText(
                "Prin continuare sunteti de acord cu cele spuse de mai sus",
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 + 50),
                True,
            )
            text.renderText(
                "Apasati tasta Enter pentru a continua",
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 + 200),
                True,
            )
            pygame.display.flip()
            clock.tick(60)

    def event_test(self, screen: Surface, clock: Clock):
        self.channel.stop()
        mainGame = MainGame(self.WIDTH, self.HEIGHT, self.script_dir)
        mainGame.loadingScreen(screen, clock, True)

    def event_test_altu(self, screen, clock):
        self.channel.stop()
        mainGame = MainGame(self.WIDTH, self.HEIGHT, self.script_dir)
        mainGame.loadingScreen(screen, clock)

    def renderMainMenu(self, screen: Surface, clock: Clock):
        self.channel.play(self.sound, -1)
        text = Text.Text(screen, None, 74)
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
            text.renderText("Cinci", "white", (50, 50))
            text.renderText("Nopti", "white", (50, 100))
            text.renderText("In", "white", (50, 150))
            text.renderText("Studentie", "white", (50, 200))

            text.renderText("New Game", "white", (50, 350 + 74 / 2))
            text.renderText("Continue", "white", (50, 450 + 74 / 2))

            screen.blit(self.bugimage, (700, -200))

            text.renderText("ALPHA 2", pygame.Color("white"), (1030, 680))
            # self.renderButtons(screen)
            pygame.display.flip()
            clock.tick(60)
