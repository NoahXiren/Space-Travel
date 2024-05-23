import pygame, sys
import random
from random import randint
from random import uniform
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('Images/rocket.png').convert_alpha()
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_frect( center =(20,120))
        self.speed = 300
        self.direction = pygame.math.Vector2()
        self.mask = pygame.mask.from_surface(self.image)

        # laser cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() 
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        
        #laser
        laser_keys = pygame.key.get_pressed()
        if laser_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midright, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()


        self.laser_timer()

class stars(pygame.sprite.Sprite):
    def __init__(self, pos, star_surf, group):
        super().__init__(group)
        self.image = star_surf 
        self.rect = self.image.get_frect(center = pos)


class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super(). __init__(group)
        self.image = surf
        self.rect = self.image.get_frect(midleft = pos)
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt):
        self.rect.centerx += 400 * dt
        if self.rect.left > 300:
            self.kill()

class Asteroids(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group):
        super().__init__(group)
        self.origin = surf
        self.image = self.origin
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 6000
        self.direction = pygame.math.Vector2(-1, uniform(-0.5, 0.5))
        self.speed = randint(50,100)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotate_speed = randint(20,50)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotate_speed * dt
        self.image = pygame.transform.rotozoom(self.origin, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos ,group):
        super().__init__(group)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.animation_speed = 9

    def update(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

def Collision():
    global game_run
    collision_sprites = pygame.sprite.spritecollide(player, Aste_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
            game_run = False
            dead_sound.play()

    for laser in laser_sprites:
        destroyed_sprites = pygame.sprite.spritecollide(laser, Aste_sprites,True, pygame.sprite.collide_mask)
        if destroyed_sprites:
            laser.kill()
            Explosion(destroyed_frames, laser.rect.midright, all_sprites)
            Explosion_sound.play()

            
 
def Display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = text_font.render(str(current_time), False,'#04eef3')
    text_rect = text_surf.get_frect(midbottom = (250/2, 240))
    Display_surf.blit(text_surf,text_rect)
    pygame.draw.rect(Display_surf, 'white', text_rect.inflate(20,10).move(0, 0), 2, 5 )


pygame.init() 
pygame.display.set_caption('Space Walk')
screen = pygame.display.set_mode((500,500))
Display_surf = pygame.Surface((250,250))
clock = pygame.time.Clock()

# variables
game_run = True 
# font
text_font = pygame.font.Font('font/pixelify_sans.ttf', 15)
# Assteroids
Asteroids_surf = pygame.image.load('Images/Aass.png').convert_alpha()
# laser
laser_surf = pygame.image.load('Images/laser.png').convert_alpha()
# star
star_surf = pygame.image.load('Images/star.png').convert_alpha()
# destroyed asteroids
destroyed_frames =  [pygame.image.load(join('Images' , 'Explosion', f'{i}.png')).convert_alpha() for i in range(8)]


# sound
laser_sound = pygame.mixer.Sound('sounds/laser_shoot.wav')
laser_sound.set_volume(0.3)

Explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
Explosion_sound.set_volume(0.3)

dead_sound = pygame.mixer.Sound('sounds/dead.wav')
dead_sound.set_volume(0.3)
# sprites
all_sprites = pygame.sprite.Group()
Aste_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    star_x = random.randint(5,245)
    star_y = random.randint(5,245)
    stars((star_x, star_y), star_surf,all_sprites)

player = Player(all_sprites)

# Asteroid timer(event)
Asteroid_event = pygame.event.custom_type() 
pygame.time.set_timer(Asteroid_event, 500) 

while game_run:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == Asteroid_event:
            Asteroid_x = randint(250,300)
            Asteroid_y = randint(0,250)
            Asteroids(Asteroids_surf,(Asteroid_x, Asteroid_y), (all_sprites, Aste_sprites))

    all_sprites.update(dt)
    Collision()
   
    Display_surf.fill('#050526')
    all_sprites.draw(Display_surf)
    Display_score()
    screen.blit(pygame.transform.scale(Display_surf, screen.get_size()),(0,0))
    pygame.display.update()
   