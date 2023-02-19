import pygame, os, math
from csv import reader
from scripts.sprite import Sprite

class Map():
    def __init__(self, tile_size, wn_size):
        self.tarrain = "assets/map/floating-islands.csv"
        self.tile_size = tile_size
        self.sprite = Sprite(pygame.image.load("assets/images/tilesets/grass-tileset.png"), (32, 32), (self.tile_size, self.tile_size))
        self.sprite_rows, self.sprite_col = 7, 7
        self.surface = pygame.Surface(wn_size)
        
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
            row = []
            for j in range(0, self.sprite_col):
                row.append(self.sprite.cut(j, i))
            self.images.append(row)
    
    def draw_map(self, scroll):
        y = 0
        for row in self.map_list:
                self.colums = 0
                self.rows += 1
                y += self.tile_size
                x = 0
                for tile in row:
                    x += self.tile_size
                    self.colums += 1
                    if tile != '-1' or tile != '0':
                        image_row = math.floor(int(tile) / self.sprite_col)
                        if image_row >= 1:
                            image_col = int(tile) % image_row
                        else:
                            image_col = int(tile)
                        self.surface.blit(self.images[image_row][image_col], (x - scroll[0], y - scroll[1]))
                    if tile == '0':
                        self.surface.blit(self.images[0][0], (x - scroll[0], y - scroll[1]))
        
        return self.surface