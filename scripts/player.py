import pygame, os, time, random
from scripts.sprite import Sprite

class Player():
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        
        self.is_jumping, self.on_ground, self.is_falling = False, False, False
        self.speed = 2
        self.double_jump = True
        self.last_jump = time.time()
        self.gravity, self.friction = .6, -.15
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        
        # animation
        self.steps = 0
        self.animation_duration = 7
        self.flight_duration = 0
        self.direction = 'right'
        self.idle_time = 0
        self.last_image = 0

        
    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.keys[pygame.K_a]:
            self.direction = 'left'
            self.acceleration.x -= self.speed
        elif self.keys[pygame.K_d]:
            self.direction = 'right'
            self.acceleration.x += self.speed
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(7)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.x = self.position.x
        self.rect.x = self.x
    
    def vertical_movement(self, dt):
        if self.keys[pygame.K_SPACE]:
            self.jump()
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        if self.on_ground: 
            self.is_falling = False
            self.is_jumping = False
            self.velocity.y = 0
        else:
            self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        if self.y - self.position.y < 0:
            self.is_falling = True
            self.is_jumping = False
        self.y = self.position.y
        self.rect.y = self.y
    
    def horizontal_collision(self, tiles):
        for tile in tiles:
            tile_rect = tile[0].get_rect()
            tile_rect.x = tile[1][0]
            tile_rect.y = tile[1][1]
            if self.rect.colliderect(tile_rect):
                if self.velocity.x > 0:  # Hit tile moving right
                    self.position.x = tile_rect.left - self.rect.w
                    self.x = self.position.x
                elif self.velocity.x < 0:  # Hit tile moving left
                    self.position.x = tile_rect.right
                    self.x = self.position.x
        self.rect.x = self.x
    
    def checkCollisionsy(self, tiles):
        print(self.rect.y - self.y)
        self.on_ground = False
        for tile in tiles:
            tile_rect = tile[0].get_rect()
            tile_rect.x = tile[1][0]
            tile_rect.y = tile[1][1]
            if self.rect.colliderect(tile_rect):
                if self.velocity.y >= 0:  # Hit tile from the top
                    self.on_ground = True
                    self.is_jumping = False
                    self.is_falling = False
                    self.velocity.y = 0
                    if self.keys[pygame.K_SPACE]:
                        self.position.y = self.y - 50
                        self.rect.y = self.position.y
                    else:
                        self.position.y = tile_rect.top
                        self.rect.bottom = self.position.y
                elif self.velocity.y < 0:  # Hit tile from the bottom
                    self.velocity.y = 0
                    self.position.y = tile_rect.bottom
                    self.rect.top = self.position.y
        
            
    
    def jump(self):
        """checks if player is able to jump and sets the velocity"""
        if self.on_ground:
            self.last_jump = time.time()
            self.double_jump = True
            self.is_jumping = True
            self.is_falling = False
            self.velocity.y -= 13
            self.rect.y = self.y
            self.on_ground = False
        elif self.double_jump and self.on_ground == False and time.time() - self.last_jump > 0.3:
            self.double_jump = False
            self.is_jumping = True
            self.is_falling = False
            self.velocity.y -= 13
            self.on_ground = False
        if self.velocity.y <= -15.5:
            self.velocity.y = -15
        
    
    def limit_velocity(self, max_vel):
        """limits the velocity of the player"""
        min(-max_vel, max(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
    def update(self, window, dt, tiles):
        self.keys = pygame.key.get_pressed()
        self.horizontal_movement(dt)
        self.horizontal_collision(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)
        self.animations()
    
    def animations(self):
        if self.is_jumping:
            if self.flight_duration <= 10:
                self.image = self.jump1
            elif self.flight_duration <= 30:
                self.image = self.jump2
            elif self.flight_duration <= 1000:
                self.image = self.jump3
            self.flight_duration += 1
        elif self.is_falling:
            if self.flight_duration <= 10:
                self.image = self.fall1
            elif self.flight_duration <= 30:
                self.image = self.fall2
            elif self.flight_duration <= 1000:
                self.image = self.fall3
            self.flight_duration += 1
        elif self.keys[pygame.K_a] or self.keys[pygame.K_d]:
            if self.steps <= self.animation_duration:
                self.image = self.run1
            elif self.steps <= self.animation_duration * 2:
                self.image = self.run2
            elif self.steps <= self.animation_duration * 3:
                self.image = self.run3
            elif self.steps <= self.animation_duration * 4:
                self.image = self.run4
            elif self.steps <= self.animation_duration * 5:
                self.image = self.run5
            elif self.steps <= self.animation_duration * 6:
                self.image = self.run6
            elif self.steps <= self.animation_duration * 7:
                self.image = self.run7
            elif self.steps >= self.animation_duration * 7 + 1:
                self.steps = 0
            self.steps += 1
        else:
            if self.idle_time >= self.animation_duration * 7 + 1:
                self.idle_time = 0
            if self.idle_time <= self.animation_duration * 5:
                self.image = self.idle
            elif self.idle_time < self.animation_duration * 7:
                self.image = self.idle_low

            self.idle_time += 1    
                            
        if self.is_jumping == False and self.is_falling == False:
            self.flight_duration = 0     
        if self.direction == 'left' and self.image != self.last_image:
            self.image = pygame.transform.flip(self.image, True, False) 
        self.last_image = self.image
        self.image.set_colorkey((0, 0, 0))
            
        
    def load_images(self):
        sprite = Sprite(pygame.image.load("assets/images/player/player_sprite.png"), (16, 32), (self.width, self.height))
        self.idle = sprite.cut(0, 0)
        self.idle_blink = sprite.cut(0, 1)
        self.idle_low = sprite.cut(1, 0)
        self.blink_low = sprite.cut(1, 1)
        
        self.run1 = sprite.cut(0, 3)
        self.run2 = sprite.cut(1, 3)
        self.run3 = sprite.cut(2, 3)
        self.run4 = sprite.cut(3, 3)
        self.run5 = sprite.cut(4, 3)
        self.run6 = sprite.cut(5, 3)
        self.run7 = sprite.cut(6, 3)
        
        self.jump1 = sprite.cut(1, 5)
        self.jump2 = sprite.cut(2, 5)
        self.jump3 = sprite.cut(3, 5)
        
        self.fall1 = sprite.cut(4, 5)
        self.fall2 = sprite.cut(5, 5)
        self.fall3 = sprite.cut(6, 5)
        
        
        self.image = self.idle
        self.last_image = self.idle
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.rect.height = self.height - (4 * 2)
        self.mask = pygame.mask.from_surface(self.image)