import pygame, sys, random, time

from scripts.player import Player
from scripts.map import Map

pygame.init()

class Game():
    def __init__(self):
        # ------------------------------------------------ display setup
        self.width, self.height = 960, 540
        # self.width, self.height = 1920, 1080
        if self.width == 1920:
            self.display = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode((self.width, self.height))
        self.window = pygame.Surface((1920, 1080))
        pygame.display.set_caption('Smash')
        
        # ------------------------------------------------ setting up variables
        self.run = True
        self.MAX_FPS = 60
        self.dt = 0
        self.last_time = time.time()
        self.scroll = [0, 0]
        self.render_offset = [0, 0]
        self.screen_shake = 0
        self.camera_smoothing = 15
        
        self.player = Player(0, 0, 64, 64)
        self.player.load_images()
        self.map = Map(32, (self.width, self.height))
        self.map.load_csv_data()
        self.map.load_images()
        self.map_surface = self.map.draw_map(self.scroll)[0]
        self.tile_list = self.map.draw_map(self.scroll)[1]
        self.clock = pygame.time.Clock()
        
    def calculate_dt(self):
        """Calculates the deltatime between each frame"""
        self.dt = time.time() - self.last_time
        self.dt *= 60
        self.camara_smoothing = 8 - int(self.dt)
        
    def events(self):
        """"checks if window was quit using the x button"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.run = False
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.screen_shake = 20
        
    def collision(self):
        self.hit_list = []
        self.player.move(self.dt, self.hit_list)
        self.collision_types = {'right': False, 'left': False, 'top': False, 'down': False}
    
        if self.player.rect.y >= 600:
            self.player.on_ground = True
        # for tile in self.tile_list:
        #     tile_mask = pygame.mask.from_surface(tile[0])
        #     collision = self.player.mask.overlap(tile_mask, (self.player.x - tile[1][0], self.player.y - tile[1][1]))
        #     if collision:
        #         self.hit_list.append(tile)
        
        # self.player.move(self.dt, self.hit_list)
        for tile in self.tile_list:
            tile_rect = tile[0].get_rect()
            tile_mask = pygame.mask.from_surface(tile[0])
            tile_rect.x = tile[1][0]
            tile_rect.x = tile[1][1]
            collision = self.player.mask.overlap(tile_mask, (self.player.x - tile[1][0], self.player.y - tile[1][1]))
            if collision:
                self.hit_list.append(tile)
            
        print(len(self.hit_list))
                
                
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
            # self.scroll[0] += int((self.player.rect.x  - self.scroll[0] - (self.width / 2)) / self.camara_smoothing)
            # self.scroll[1] += int((self.player.rect.y - self.scroll[1] - (self.height / 2)) / self.camara_smoothing)
            
            # ------------------------------------------------ drawing
            if self.screen_shake > 0:
                self.screen_shake -= 1
            self.render_offset = [0, 0]
            if self.screen_shake:
                self.render_offset[0] = random.randint(0, 8) - 4
                self.render_offset[1] = random.randint(0, 8) - 4
            
            self.window.fill((0, 0, 0))
            self.window.blit(self.map_surface, (0 - self.scroll[0], 0 - self.scroll[1]))
            self.player.update(self.dt)          
            self.window.blit(self.player.image, ((self.player.x - (self.player.width / 2))- self.scroll[0], (self.player.y - (self.player.height / 2)) - self.scroll[1]))
            self.display.blit(pygame.transform.scale(self.window, (self.width, self.height)), self.render_offset)
    
            # ------------------------------------------------ update
            self.last_time = time.time() 
            pygame.display.update()
                

game = Game()
game.loop()