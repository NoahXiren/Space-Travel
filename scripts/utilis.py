import pygame
import os

BASE_PATH = 'Images/'

def load_image(path):
    PATH = BASE_PATH + path
    img = pygame.image.load(PATH).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_PATH + path):
        full_path = os.path.join(BASE_PATH, path, img_name)
        if os.path.isfile(full_path):
            images.append(load_image(os.path.join(path, img_name)))
        elif os.path.isdir(full_path):
            images.extend(load_images(os.path.join(path, img_name)))
    return images

class Animation:
    def __init__(self, images, img_dur =5, loop = True):
        self.images =  images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))

        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
    
        
