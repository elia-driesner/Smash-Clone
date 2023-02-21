import pygame, os, math
from csv import reader
from scripts.sprite import Sprite

class Map():
    def __init__(self, tile_size, wn_size):
        self.tarrain = "assets/map/floating-islands.csv"
        self.tile_size = tile_size
        self.sprite = Sprite(pygame.image.load("assets/images/tilesets/grass-tileset.png"), (32, 32), (self.tile_size, self.tile_size))
        self.sprite_rows, self.sprite_col = 7, 7
        self.surface = pygame.Surface((1920, 1080))
        self.wn_size = wn_size
        
        self.images = []
        
    def load_csv_data(self):
        # ---------------------------------------------------------------- Load the map data from csv file
        self.rows = 0
        self.colums = 0
        self.map_list = []
        with open (self.tarrain) as map:
            level = reader(map, delimiter = ",")
            for row in level:
                self.map_list.append(list(row))
            
    def load_images(self):
        for i in range(0, self.sprite_rows):
            for j in range(0, self.sprite_col):
                self.images.append(self.sprite.cut(j, i))
    
    def draw_map(self, scroll):
        self.tile_list = []
        spawn = (0, 0)
        y = 0
        for row in self.map_list:
                self.colums = 0
                self.rows += 1
                y += self.tile_size
                x = 0
                for tile in row:
                    x += self.tile_size
                    self.colums += 1
                    if tile != '-1' and tile != '39':
                            self.surface.blit(self.images[int(tile)], (x - scroll[0], y - scroll[1]))
                            self.tile_list.append([self.images[int(tile)], (x - scroll[0], y - scroll[1])])
                    if tile == '39':
                        spawn = (x, y)
        
        return [self.surface, self.tile_list, spawn]