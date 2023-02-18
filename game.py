import pygame, sys
import time

from scripts.player import Player

pygame.init()

class Game():
    def __init__(self):
        # self.width, self.height = 960, 540
        self.width, self.height = 1920, 1080
        self.window = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption('Smash')
        self.run = True
        self.MAX_FPS = 60
        self.dt = 0
        self.last_time = time.time()
        
        self.player = Player(100, 100, 40, 40)
        self.clock = pygame.time.Clock()
        
    def calculate_dt(self):
        self.dt = time.time() - self.last_time
        self.dt *= 60

        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
                sys.exit(0)
        
    def collision(self):
        if self.player.rect.y >= 600:
            self.player.on_ground = True
                
    def loop(self):
        while self.run:
            self.clock.tick(self.MAX_FPS)
            self.calculate_dt()
            self.window.fill((0, 0, 0))
            self.events()
            self.collision()
            self.player.update(self.window, self.dt)
            self.last_time = time.time()
            
            pygame.display.update()
                

game = Game()
game.loop()