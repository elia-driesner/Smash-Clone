import pygame, sys, random, time, asyncio
from _thread import * 

from scripts.player import Player
from scripts.map import Map
from networking.network import Network

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
        
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        
        # ------------------------------------------------ setting up variables
        self.run = True
        self.MAX_FPS = 60
        self.dt = 0
        self.last_time = time.time()
        self.scroll = [0, 0]
        self.render_offset = [0, 0]
        self.screen_shake = 0
        self.camera_smoothing = 15
        
        # start_new_thread(self.connect_client, ())
        self.n = Network()
        
        self.clock = pygame.time.Clock()
        
        # ------------------------------------------------ setting up player and map
        self.player = Player(100, 100, 16, 32)
        self.enemy = Player(100, 100, 16, 32)
        self.enemy_pos = (self.enemy.x, self.enemy.y)
        self.map = Map(16, (self.width, self.height))
        self.player_map_init()
    
    # def connect_client(self):
    #     self.client = Network()
    #     print('connecting...')
    #     while self.client.connected == False:
    #         time.sleep(100)
    #         self.cleint.connect()
    #         print('connecting...')
        
        
    def loop(self):
        """game loop"""
        while self.run:
            # ------------------------------------------------ pygame events
            self.clock.tick(self.MAX_FPS)
            self.calculate_dt()
            self.events()
            self.player.update(self.window, self.dt, self.tile_list)
            self.enemy_pos = self.read_pos(self.n.send(self.make_pos ((self.player.x, self.player.y))))
            self.enemy,x, self.enemy.y = self.enemy_pos[0], self.enemy_pos[1]
            self.enemy.rect.x, self.enemy.rect.y = self.enemy.x, self.enemy.y
            
            # ------------------------------------------------ moving the camera
            self.scroll[0] += int((self.player.rect.x  - self.scroll[0] - (self.width / 2)) / self.camara_smoothing)
            self.scroll[1] += int((self.player.rect.y - self.scroll[1] - (self.height / 2)) / self.camara_smoothing)
            
            if self.player.shake and self.player.on_ground: 
                self.screen_shake = 2
                self.player.shake = False
            
            # ------------------------------------------------ drawing          
            self.window.fill((0, 0, 0))
            self.window.blit(self.map_surface, (0 - self.scroll[0], 0 - self.scroll[1]))
            self.window.blit(self.player.image, ((self.player.rect.x)- self.scroll[0], (self.player.rect.y) - self.scroll[1]))
            self.window.blit(self.enemy.image, ((self.enemy.rect.x)- self.scroll[0], (self.enemy.rect.y) - self.scroll[1]))
            # pygame.draw.rect(self.window, (255, 255, 255), self.player.rect)
            self.text = self.font.render(str(int(self.clock.get_fps())) + ' FPS', True, (255, 255, 255))
            self.window.blit(self.text, (10, 10))
            self.display.blit(pygame.transform.scale(self.window, (self.width, self.height)), self.render_offset)
    
            
            self.last_time = time.time() 
            pygame.display.update()
    
    def calculate_dt(self):
        """Calculates the deltatime between each frame"""
        self.dt = time.time() - self.last_time
        self.dt *= 60
        self.camara_smoothing = 8 - int(self.dt)
        
    def read_pos(self, str):
        str = str.split(",")
        print(str)
        return int(str[0]), int(str[1])

    def make_pos(self, tuple):
        return str(tuple[0]) + "," + str(tuple[1])
        
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
        
        # shakes the screen if screen_shake > 0
        if self.screen_shake > 0:
            self.screen_shake -= 1
            self.render_offset = [0, 0]
            if self.screen_shake:
                self.render_offset[0] = random.randint(0, 8) - 4
                self.render_offset[1] = random.randint(0, 8) - 4
    
    def player_map_init(self):
        self.map.load_csv_data()
        self.map.load_images()
        self.map_output = self.map.draw_map(self.scroll)
        self.tile_list = self.map_output[1]
        self.map_surface = self.map_output[0]
        
        self.enemy.load_images()
        self.enemy_spawn = self.map_output[3]
        self.enemy.x, self.enemy.y = self.enemy_spawn[0], self.enemy_spawn[1]
        self.enemy.rect.x, self.enemy.rect.y = self.enemy.x, self.enemy.y
        self.enemy.position.x, self.enemy.position.y = self.enemy.x, self.enemy.y
        self.enemy.spawn = self.enemy_spawn
        
        self.player.load_images()
        self.player_spawn = self.map_output[2]
        self.player.x, self.player.y = self.player_spawn[0], self.player_spawn[1]
        self.player.rect.x, self.player.rect.y = self.player.x, self.player.y
        self.player.position.x, self.player.position.y = self.player.x, self.player.y
        self.player.spawn = self.player_spawn

                
game = Game()
game.loop()