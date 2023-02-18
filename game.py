import pygame, sys
import time

from scripts.player import Player

pygame.init()

class Game():
    def __init__(self):
        # ------------------------------------------------ display setup
        # self.width, self.height = 960, 540
        self.width, self.height = 1920, 1080
        self.display = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.window = pygame.Surface((self.width, self.height))
        pygame.display.set_caption('Smash')
        
        # ------------------------------------------------ setting up variables
        self.run = True
        self.MAX_FPS = 60
        self.dt = 0
        self.last_time = time.time()
        self.scroll = [0, 0]
        self.camera_smoothing = 15
        
        self.player = Player(100, 100, 50, 50)
        self.player.load_images()
        self.clock = pygame.time.Clock()
        
    def calculate_dt(self):
        """Calculates the deltatime between each frame"""
        self.dt = time.time() - self.last_time
        self.dt *= 60
        self.camara_smoothing = 15 - int(self.dt)
        
    def events(self):
        """"checks if window was quit using the x button"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
                sys.exit(0)
        
    def collision(self):
        """collision detection"""
        if self.player.rect.y >= 600:
            self.player.on_ground = True

                
    def loop(self):
        """game loop"""
        while self.run:
            # ------------------------------------------------ pygame events
            self.clock.tick(self.MAX_FPS)
            self.calculate_dt()
            self.events()
            
            # ------------------------------------------------ collision events
            self.collision()
            
            # ------------------------------------------------ moving the camera
            self.scroll[0] += int((self.player.rect.x  - self.scroll[0] - (self.width / 2)) / self.camara_smoothing)
            self.scroll[1] += int((self.player.rect.y - self.scroll[1] - (self.height / 2)) / self.camara_smoothing)
            
            # ------------------------------------------------ drawing
            self.window.fill((0, 0, 0))
            self.player.update(self.window, self.dt)
            self.window.blit(self.player.image, ((self.player.rect.x - (self.player.width / 2))- self.scroll[0], (self.player.rect.y - (self.player.height / 2)) - self.scroll[1]))
            self.display.blit(self.window, (0, 0))
            
            # ------------------------------------------------ update
            self.last_time = time.time() 
            pygame.display.update()
                

game = Game()
game.loop()