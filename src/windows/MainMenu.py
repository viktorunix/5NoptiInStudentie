import threading

import cv2
import pygame
from pygame import Surface
from pygame.time import Clock

from gui import Text
from gui.Button import Button
from gui.VideoBackground import VideoBackground
from utils.stateLoader import get_resource_path
from windows.MainGame import MainGame


class MainMenu:
    running = True
    buttons = []

    def load_assets(self):
        self.cap = cv2.VideoCapture(get_resource_path("/assets/videos/mainmenu.mp4"))

    def loader(self):
        self.load_assets()

    def __init__(self, WIDTH: int, HEIGHT: int):
        print("incepe")
        self.video_background = VideoBackground(
            get_resource_path("/assets/videos/mainmenu.mp4"), WIDTH, HEIGHT
        )
        print("terminat")
        self.sound = None
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.cap: cv2.VideoCapture = cv2.VideoCapture()
        self.channel = pygame.mixer.find_channel()
        self.another_channel = pygame.mixer.find_channel()
        self.bugimage = pygame.image.load(
            get_resource_path("/assets/images/mainmenuanimatronic.png")
        ).convert_alpha()
        self.bugimage.set_alpha(180)
        self.bugimage = pygame.transform.scale(
            self.bugimage,
            (
                self.bugimage.get_width() * (self.HEIGHT / 360),
                self.bugimage.get_height() * (self.HEIGHT / 360),
            ),
        )

        self.buttons.append(
            Button(
                (self.WIDTH / 4, self.HEIGHT / 18),
                (self.WIDTH / 25, self.HEIGHT / 2 + self.HEIGHT / 16),
                self.event_test,
            )
        )
        self.buttons.append(
            Button(
                (self.WIDTH / 5, self.HEIGHT / 18),
                (self.WIDTH / 25, self.HEIGHT / 2 + self.HEIGHT / 6),
                self.event_test_altu,
            )
        )

        self.sound = pygame.mixer.Sound(get_resource_path("/assets/audio/mainmenu.mp3"))

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
            get_resource_path("/assets/audio/easteregg.mp3")
        )
        self.another_channel = pygame.mixer.find_channel()
        self.another_channel.play(easter_egg_sound)
        # fontSize = self.HEIGHT // 15
        is_enter: bool = False
        while not loaded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_enter = True
            # ret, frame = self.cap.read()
            if is_enter:
                loaded = True
            try:
                image = pygame.image.load(
                    get_resource_path("/assets/images/warningscreen.jpeg")
                )
                image = pygame.transform.scale(image, (self.WIDTH, self.HEIGHT))
                image.set_alpha(120)
                screen.blit(image, (0, 0))
                # font = pygame.font.Font(None, self.HEIGHT // 20)
            except Exception as e:
                print("Warning screen background image not found")
            text = Text.Text(screen, fontSize=100)
            text.renderText(
                "ATENTIE!!",
                "red",
                (self.WIDTH / 2, self.HEIGHT / 2 - 2 * text.fontSize),
                True,
            )
            text = Text.Text(screen)
            text.renderText(
                "Acest joc este o parodie si trebuie tratat ca atare",
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 - text.fontSize),
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
                (self.WIDTH / 2, self.HEIGHT / 2 + text.fontSize),
                True,
            )
            text.renderText(
                "Apasati tasta Enter pentru a continua",
                "white",
                (self.WIDTH / 2, self.HEIGHT / 2 + 3 * text.fontSize),
                True,
            )
            pygame.display.flip()
            clock.tick(60)

    def event_test(self, screen: Surface, clock: Clock):
        self.channel.stop()
        mainGame = MainGame(self.WIDTH, self.HEIGHT, self.video_background)
        mainGame.loadingScreen(screen, clock, True)
        self.channel.play(self.sound, -1)

    def event_test_altu(self, screen, clock):
        self.channel.stop()
        mainGame = MainGame(self.WIDTH, self.HEIGHT, self.video_background)
        mainGame.loadingScreen(screen, clock)
        self.channel.play(self.sound, -1)

    def renderMainMenu(self, screen: Surface, clock: Clock):
        self.channel.play(self.sound, -1)
        text = Text.Text(screen, fontSize=120)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        button.mouse_click_handler(event.pos, screen, clock)
            self.video_background.static_update(screen)
            horizontalOffset = self.WIDTH / 25
            verticalOffset = self.HEIGHT / 20
            text.renderText("Cinci", "white", (horizontalOffset, verticalOffset))
            text.renderText(
                "Nopti",
                "white",
                (horizontalOffset, verticalOffset + text.fontSize * 0.75),
            )
            text.renderText(
                "In", "white", (horizontalOffset, verticalOffset + text.fontSize * 1.5)
            )
            text.renderText(
                "Studentie",
                "white",
                (horizontalOffset, verticalOffset + text.fontSize * 2.25),
            )

            text.renderText(
                "New Game",
                "white",
                (horizontalOffset, self.HEIGHT / 2 + self.HEIGHT / 16),
            )
            text.renderText(
                "Continue",
                "white",
                (horizontalOffset, self.HEIGHT / 2 + self.HEIGHT / 6),
            )

            screen.blit(self.bugimage, (self.WIDTH / 2, -self.HEIGHT / 10))
            # self.renderButtons(screen)
            text.renderText(
                "Release 1.0",
                pygame.Color("white"),
                (self.WIDTH * 23 / 25, self.HEIGHT * 24 / 25),
                True,
            )
            # self.renderButtons(screen)
            pygame.display.flip()
            clock.tick(60)
