import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self,
                  group: pygame.sprite.Sprite ,
                  pos :list[int],
                  color: str,
                  direction: pygame.math.Vector2,
                  speed: int):
        super().__init__(group)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed  = speed

        self.create_surface()

    def create_surface(self):
        self.image = pygame.Surface((4,4)).convert_alpha()
        self.image.set_colorkey('black')
        pygame.draw.circle(surface=self.image, color=self.color ,center=(2,2), radius=2)
        self.rect = self.image.get_frect(center = self.pos)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def check_pos(self):
        if self.pos[0] < -50:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.check_pos()
