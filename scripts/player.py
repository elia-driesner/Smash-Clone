import pygame, os

class Player():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('assets/images/player/idle/', 'player-idle.png')), (16, 16))
        self.rect = self.image.get_rect()
        self.speed = 5
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        elif keys[pygame.K_d]:
            self.x += self.speed
                
        self.rect.x = self.x
        self.rect.y = self.y