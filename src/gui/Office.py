import pygame
from gui.OfficeButton import OfficeButton
class Office:
    def __init__(self, WIDTH, HEIGHT, script_dir: str):
        self.__script_dir = script_dir
        self.office = pygame.image.load(script_dir + "/assets/images/office_front_lights.jpeg")
        scale_factor = HEIGHT / self.office.get_height()
        new_width = int(self.office.get_width() * scale_factor)
        self.office = pygame.transform.scale(self.office, (new_width, HEIGHT))
        self.office_width = self.office.get_width()
        self.__width = WIDTH
        self.__height = HEIGHT
        self.camera_x = 0
        self.scroll_speed = 5
        #TODO: SCHIMBA NAIBI LINIA ASTA CA E LA MISTO
        self.__camera_button = OfficeButton(pygame.Color("red"), self.__width - 600, self.__height - 120, 500, 100)
        self.__back_office_button = OfficeButton(pygame.Color("red"), 50, self.__height - 700, 100, 500)
        self.__laptop_button = OfficeButton(pygame.Color("red"), self.__width - 1200, self.__height - 120, 500, 100)
        run = True
        clock = pygame.time.Clock()
    def test(self, screen, clock):
        print("mergeeee")


    def get_camera_button(self) -> OfficeButton:
        return self.__camera_button
    def get_back_office_button(self) -> OfficeButton:
        return self.__back_office_button
    def get_laptop_button(self) -> OfficeButton:
        return self.__laptop_button

    def render_office(self,screen):
        mouse_pos = pygame.mouse.get_pos()
        if(mouse_pos[0] < 100):
            self.camera_x -= self.scroll_speed
        if(mouse_pos[0] > self.__width - 100):
            self.camera_x += self.scroll_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_x -= self.scroll_speed
        if keys[pygame.K_RIGHT]:
            self.camera_x += self.scroll_speed
        self.camera_x = 0 if self.camera_x < 0 else self.camera_x
        self.camera_x = self.office_width - self.__width if self.camera_x > self.office_width - self.__width else self.camera_x

        view_rect = pygame.Rect(self.camera_x, 0, self.__width, self.__height)
        screen.blit(self.office, (0,0), view_rect)
        self.__camera_button.render_button(screen)
        self.__laptop_button.render_button(screen)
        if(self.camera_x == 0):
            self.__back_office_button.render_button(screen)
