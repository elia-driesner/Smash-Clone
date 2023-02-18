import pygame, os, time
from scripts.sprite import Sprite

class Player():
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        
        self.is_jumping, self.on_ground = False, False
        self.speed = 2
        self.double_jump = True
        self.last_jump = time.time()
        self.gravity, self.friction = .32, -.15
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

        
    def move(self, dt):
        """player movement and jumping and falling physics"""
        self.acceleration.x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration.x -= self.speed
        elif keys[pygame.K_d]:
            self.acceleration.x += self.speed
        if keys[pygame.K_SPACE]:
            self.jump()
            
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.x = self.position.x
        
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        if self.on_ground: 
            self.velocity.y = 0
        else:
            self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.y = self.position.y
                
        self.rect.x = self.x
        self.rect.y = self.y
    
    def jump(self):
        """checks if player is able to jump and sets the velocity"""
        if self.on_ground:
            self.last_jump = time.time()
            self.double_jump = True
            self.is_jumping = True
            self.velocity.y -= 12
            self.on_ground = False
        elif self.double_jump and self.on_ground == False and time.time() - self.last_jump > 0.3:
            self.double_jump = False
            self.is_jumping = True
            self.velocity.y -= 12
            self.on_ground = False
        if self.velocity.y <= -12.5:
            self.velocity.y = -12
        
    
    def limit_velocity(self, max_vel):
        """limits the velocity of the player"""
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
    def update(self, window, dt):
        self.move(dt)
    
    def animations(self):
        pass
        
    def load_images(self):
        sprite = Sprite(pygame.image.load("assets/images/player/player_sprite.png"), (32, 32), (self.width, self.height))
        self.idle = sprite.cut(0, 0)
        self.idle_blink = sprite.cut(0, 1)
        
        
        self.image = self.idle
        self.rect = self.image.get_rect()