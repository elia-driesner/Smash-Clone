import pygame

class Sprite:
    def __init__(self, image, size, scale, colorkey ="1"):
        self.sprite = image
        self.width = size[0]
        self.height = size[1]
        self.size = size
        self.scale = scale
        self.colorkey = colorkey
        if not colorkey == "1":
            self.colorkey = colorkey
        

    def cut(self, frame, layer):
        image = pygame.Surface((self.width, self.height))
        image.blit(self.sprite, (0, 0), ((frame * self.width), (self.height * layer), self.width, self.height))
        image = pygame.transform.scale((image), self.scale)
        
        if not self.colorkey == "1":
            image.set_colorkey(self.colorkey)
        
        return image.convert_alpha()