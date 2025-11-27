import pygame

class Office:

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
        
        run = True
        clock = pygame.time.Clock()

    def render_office(self,screen):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_x -= self.scroll_speed
        if keys[pygame.K_RIGHT]:
            self.camera_x += self.scroll_speed

        self.camera_x = 0 if self.camera_x < 0 else self.camera_x
        self.camera_x = self.office_width - self.width if self.camera_x > self.office_width - self.width else self.camera_x

        view_rect = pygame.Rect(self.camera_x, 0, self.width, self.height)
        screen.blit(self.office, (0,0), view_rect)
