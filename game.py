import pygame
import sys

class Game():
    def __init__(self):
        self.width, self.height = 960, 540
        self.window = pygame.display.set_mode((self.width, self.height))
        self.run = True
        
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