import pygame
from gui.OfficeButton import OfficeButton
class Office:
    def alttest(self, screen, clock):
        print("poate asta merge")
    def __init__(self, WIDTH, HEIGHT, script_dir: str):
        self.script_dir = script_dir
        self.office = pygame.image.load(script_dir + "/assets/images/office_front_lights.jpeg")
        scale_factor = HEIGHT / self.office.get_height()
        new_width = int(self.office.get_width() * scale_factor)
        self.office = pygame.transform.scale(self.office, (new_width, HEIGHT))
        self.office_width = self.office.get_width()
        self.width = WIDTH
        self.height = HEIGHT
        self.camera_x = 0
        self.scroll_speed = 5
        #TODO: SCHIMBA NAIBI LINIA ASTA CA E LA MISTO
        self.camera_button = OfficeButton(140, self.width - 600, self.height - 120, 500, 100, self.alttest)
        self.back_office_button = OfficeButton(140, 50, self.height - 500, 100, 500, self.alttest)
        run = True
        clock = pygame.time.Clock()
    def test(self, screen, clock):
        print("mergeeee")

    def render_office(self,screen):
        mouse_pos = pygame.mouse.get_pos()
        if(mouse_pos[0] < 100):
            self.camera_x -= self.scroll_speed
        if(mouse_pos[0] > self.width - 100):
            self.camera_x += self.scroll_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_x -= self.scroll_speed
        if keys[pygame.K_RIGHT]:
            self.camera_x += self.scroll_speed
        self.camera_x = 0 if self.camera_x < 0 else self.camera_x
        self.camera_x = self.office_width - self.width if self.camera_x > self.office_width - self.width else self.camera_x

        view_rect = pygame.Rect(self.camera_x, 0, self.width, self.height)
        screen.blit(self.office, (0,0), view_rect)
        self.camera_button.render_button(screen)
        if(self.camera_x == 0):
            self.back_office_button.render_button(screen)
