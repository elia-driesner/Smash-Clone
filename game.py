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
        
        self.player = Player(100, 100, 40, 40)
        self.clock = pygame.time.Clock()
        
    def calculate_dt(self):
        """Calculates the deltatime between each frame"""
        self.dt = time.time() - self.last_time
        self.dt *= 60
        
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
            
            # ------------------------------------------------ drawing
            self.window.fill((0, 0, 0))
            self.player.update(self.window, self.dt)
            self.display.blit(self.window, (0, 0))
            
            # ------------------------------------------------ update
            self.last_time = time.time() 
            pygame.display.update()
                

game = Game()
game.loop()