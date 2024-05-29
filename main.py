import pygame, sys
import random
from random import randint, choice
from random import uniform
from os.path import join
from scripts.particle import Particle
from scripts.utilis import load_image, load_images, Animation
from scripts.constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, group, laser_surf, laser_sound, all_sprites, laser_sprites, particle_group, player_image):
        super().__init__(group)
        self.image = player_image
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_frect( center =(20,120))
        self.speed = 300
        self.direction = pygame.math.Vector2()
        self.mask = pygame.mask.from_surface(self.image)
        self.laser_surf = laser_surf
        self.laser_sound = laser_sound
        self.all_sprites = all_sprites
        self.laser_sprites = laser_sprites
        self.particle_group = particle_group

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
            Laser(self.laser_surf, self.rect.midright, (self.all_sprites, self.laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            self.laser_sound.play()

        # SPAWN PARTICLES
        
        if self.direction.y != 0:
            self.spawn_particles(self.rect.midleft)


        self.laser_timer()

    def spawn_particles(self, pos):
        for i in range(5):
            color = choice(('red', 'yellow', 'orange'))
            direction = pygame.math.Vector2(uniform(-1,-0.5), uniform(-0.5, 0.5))
            direction = direction.normalize()
            speed = randint(50,400)
            Particle(self.particle_group, pos, color, direction, speed)


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



# GAME class
class Game:
    def __init__(self):   
        pygame.init() 
        pygame.display.set_caption('Space Walk')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.Display_surf = pygame.Surface((250,250))
        self.clock = pygame.time.Clock()
        self.state = GAME_OVER # initial state
        self.start_timer = 0 # to track the start time of the game
        self.current_time = 0 # to track the current time elapsed

        # dictionary
        self.assets = {    
            'font': pygame.font.Font('font/pixelify_sans.ttf', 15),
            'asteroid':load_image('Aass.png'),
            'laser': load_image('laser.png'),
            'star': load_image('star.png'),
            'explosion_frames': load_images('Explosion'),
            'laser_sound': pygame.mixer.Sound('sounds/laser_shoot.wav'),
            'explosion_sound': pygame.mixer.Sound('sounds/explosion.wav'),
            'dead_sound': pygame.mixer.Sound('sounds/dead.wav'),
            'player': load_image('rocket.png'),
            'start_BG': load_image('BG.png')
        }

        # volumes of sound
        self.assets['laser_sound'].set_volume(0.3)
        self.assets['explosion_sound'].set_volume(0.3)
        self.assets['dead_sound'].set_volume(0.3)

        # font
        self.text_font = self.assets['font']
        

        # sprites
        self.all_sprites = pygame.sprite.Group()
        self.Aste_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()

        for i in range(20):
            star_x = random.randint(5,245)
            star_y = random.randint(5,245)
            stars((star_x, star_y), self.assets['star'], self.all_sprites)

        self.player = Player(self.all_sprites,
                            self.assets['laser'],
                            self.assets['laser_sound'], 
                            self.all_sprites, 
                            self.laser_sprites, 
                            self.particle_group,
                            self.assets['player']
                            )



        # Asteroid timer(event)
        self.Asteroid_event = pygame.event.custom_type() 
        pygame.time.set_timer(self.Asteroid_event, 500) 

        # particle event
        self.particle_event = pygame.event.custom_type()
        pygame.time.set_timer(self.particle_event,50)


    # kill asteroids
    def clear_asteroids(self):
        for asteroid in self.Aste_sprites:
            asteroid.kill()


    # collision
    def Collision(self):
        self.collision_sprites = pygame.sprite.spritecollide(self.player, self.Aste_sprites, False, pygame.sprite.collide_mask)
        if self.collision_sprites:
                self.state = GAME_OVER
                self.assets['dead_sound'].play()

        for laser in self.laser_sprites:
            destroyed_sprites = pygame.sprite.spritecollide(laser, self.Aste_sprites,True, pygame.sprite.collide_mask)
            if destroyed_sprites:
                laser.kill()
                Explosion(self.assets['explosion_frames'], laser.rect.midright, self.all_sprites)
                self.assets['explosion_sound'].play()

    # score
    def Display_score(self):
        self.text_surf = self.text_font.render(str(self.current_time), False,'#04eef3')
        self.text_rect = self.text_surf.get_frect(midbottom = (250/2, 240))
        self.Display_surf.blit(self.text_surf,self.text_rect)
        pygame.draw.rect(self.Display_surf, 'white', self.text_rect.inflate(20,10).move(0, 0), 2, 5 )   
    
    
    # games_start_screen
    def start_screen(self):
        self.screen.blit(self.assets['start_BG'],(0,0))
        mos = pygame.mouse.get_pos()
        self.font = pygame.font.Font('font/Rubik.ttf', 40)
        
        # text_surface
        self.start_text = self.font.render('Start', False, (255,255,255))
        self.option_text = self.font.render('Option', False, (255,255,255))
        self.exit_text = self.font.render('Exit', False, (255,255,255))

        # text position
        self.start_pos = (200, 170)
        self.option_pos = (200, 230)
        self.exit_pos = (200, 290)

        # RECT
        self.button_start = self.start_text.get_frect(center = self.start_pos)
        self.button_option = self.option_text.get_frect(center = self.option_pos)
        self.button_exit = self.exit_text.get_frect(center = self.exit_pos)

    
        # condition
        # check hover
        if self.button_start.collidepoint(mos):
            self.start_text = self.font.render('Start', False, 'Red')
        if self.button_option.collidepoint(mos):
            self.option_text = self.font.render('Option', False, 'Red')
        if self.button_exit.collidepoint(mos):
            self.exit_text = self.font.render('Exit', False, 'Red')


        # blit
        self.screen.blit(self.start_text, self.start_pos)
        self.screen.blit(self.option_text, self.option_pos)
        self.screen.blit(self.exit_text, self.exit_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_start.collidepoint(mos):
                    self.state = GAME_RUN
                    self.start_timer = pygame.time.get_ticks()
                elif self.button_option.collidepoint(mos):
                    print('option clicked')

                elif self.button_exit.collidepoint(mos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


    # gameplay
    def game_run(self):
        
        dt = self.clock.tick() / 1000
        self.current_time= (pygame.time.get_ticks() - self.start_timer) // 1000 # update timer to sec form  millisecond
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == self.Asteroid_event:
                if self.state == GAME_RUN:
                    Asteroid_x = randint(250,300)
                    Asteroid_y = randint(0,250)
                    Asteroids(self.assets['asteroid'],(Asteroid_x, Asteroid_y), (self.all_sprites, self.Aste_sprites))

            if event.type == self.particle_event:
                self.player.spawn_particles(self.player.rect.midleft)


        self.all_sprites.update(dt)

        self.Collision()

        self.Display_surf.fill('#050526')
        self.all_sprites.draw(self.Display_surf)

        self.particle_group.draw(self.Display_surf)
        self.particle_group.update(dt)
            
        self.Display_score()
        self.screen.blit(pygame.transform.scale(self.Display_surf, self.screen.get_size()),(0,0))
        pygame.display.update()
        
    
    # game over
    def game_over_screen(self):
        self.screen.fill((4,150,140))
        self.font = pygame.font.Font('font/pixelify_sans.ttf', 60)
        
        # Game over text
        self.text = self.font.render('GAME_OVER', False,('#050526'))
        self.screen.blit(self.text,(90,100))

        # score
        self.show_score = self.font.render(f'Score: {str(self.current_time)}', False,'#ffffff')
        self.screen.blit(self.show_score, (140,170))
        
        # restart
        self.msg_font = pygame.font.Font('font/Rubik.ttf', 20)
        self.msg = self.msg_font.render('PRESS R TO RESTART', False, '#ffffff')
        self.screen.blit(self.msg,(150,250))        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = START_SCREEN
                    self.current_time = 0 # reset the timer
                    self.clear_asteroids() # remove all asteroids
                    return
                

        pygame.display.flip()


    def run(self):
        while True:
            if self.state == START_SCREEN:
                self.start_screen()
            elif self.state == GAME_RUN:
                self.game_run()
            elif self.state == GAME_OVER:
                self.game_over_screen()


if __name__ == "__main__":
    game = Game()
    game.run()