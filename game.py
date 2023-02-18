import pygame
import sys

from scripts.player import Player

class Game():
    def __init__(self):
        self.width, self.height = 960, 540
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Platformer')
        self.run = True
        
        self.player = Player(100, 100)
        
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
                sys.exit(0)
                
    def loop(self):
        while self.run:
            self.events()
                

game = Game()
game.loop()